select * from T2DM_PT limit 5;

create or replace table T2DM_PT_DEMO as 
select a.patid,
       a.cd_date1 as index_date,
       a.dx1_date,
       case when a.endpt_dkd_days is not null then 1 else 0 end as dia_nephr,
       a.endpt_dkd_days as time2_dia_nephr,
       case when a.endpt_dr_days is not null then 1 else 0 end as dia_retino,
       a.endpt_dr_days as time2_dia_retino,
       case when a.endpt_dn_days is not null then 1 else 0 end as dia_neuro,
       a.endpt_dn_days as time2_dia_neuro, 
       case when a.endpt_dcvd_days is not null then 1 else 0 end as dia_heart,
       a.endpt_dcvd_days as time2_dia_heart, 
       round(datediff(day,p.birth_date,a.cd_date1)/365.25) as age_at_index,
       p.sex,
        CASE WHEN p.race IN ('05') THEN 'white' 
             WHEN p.race IN ('03') THEN 'black'
             WHEN p.race IN ('02') THEN 'asian'
             WHEN p.race IN ('01') THEN 'aian'
             WHEN p.race IN ('04') THEN 'nhopi'
             WHEN p.race IN ('06') THEN 'multi'
             WHEN p.race IN ('OT') THEN 'other'
             ELSE 'NI' 
        END AS race, 
        CASE WHEN p.hispanic = 'Y' THEN 'h' 
            WHEN p.hispanic = 'N' THEN 'nh' 
            ELSE 'NI' 
        END AS hispanic
from T2DM_PT a 
join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_DEMOGRAPHIC p
on a.patid = p.patid 
;

select count(*), count(distinct patid) from T2DM_PT_DEMO;

create or replace table cov_smk as 
with smk_stk as (
    -- SMOKING from VITAL table
    select distinct
            r.PATID
            ,'SMOKING' as SDOH_VAR
            ,v.SMOKING as SDOH_VAL
            ,v.MEASURE_DATE as REPORT_DATE
            ,datediff(day,r.cd_date1,v.measure_date) as DAYS_SINCE_INDEX
    from T2DM_PT r 
    join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_VITAL v on r.patid = v.patid
    where v.SMOKING in (
        '01', --Current every day smoker  
        '02', --Current some day smoker  
        -- '03', --Former smoker   
        '05', --Smoker, current  status unknown  
        '07', --Heavy tobacco smoker  
        '08' --Light tobacco smoker  
    )
    UNION
    select  distinct 
            r.PATID
            ,'SMOKING' as SDOH_VAR
            ,os.obsclin_result_text as SDOH_VAL
            ,os.OBSCLIN_START_DATE
            ,datediff(day,r.cd_date1,os.OBSCLIN_START_DATE) as DAYS_SINCE_INDEX
    from T2DM_PT r
    join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_OBS_CLIN os on r.patid = os.patid
    where
        os.OBSCLIN_TYPE = 'LC' and 
        os.OBSCLIN_CODE in (
            '8663-7'  -- Cigarettes smoked current (pack per day) - Reported
        )
)
,smk_ordered as (
    select distinct patid, 1 as smoker_ind, 
    row_number() over (partition by patid order by abs(days_since_index)) as rn
    from smk_stk
)
select a.patid,
       coalesce(b.smoker_ind,0) as smoker_ind
from T2DM_PT a
left join smk_ordered b
on a.patid = b.patid and b.rn = 1
;

select count(distinct patid), count(*) from cov_smk;

create or replace table cov_bmi as 
with bmi_stk as (
    -- height (m)--
    SELECT r.patid,
            b.measure_date::date as measure_date,
            round(datediff(day,r.cd_date1,b.measure_date::date)/365.25) as days_since_index,
            'HT'as measure_type,b.ht/39.37 as measure_num -- default at 'in'
    FROM T2DM_PT r
    JOIN DEIDENTIFIED_PCORNET_CDM.CDM.DEID_VITAL b 
    ON r.patid = b.patid
    WHERE b.ht is not null
    UNION
    select r.patid,
            oc.OBSCLIN_START_DATE::date,
            round(datediff(day,r.cd_date1,oc.OBSCLIN_START_DATE::date)/365.25),'HT',
            case when lower(oc.OBSCLIN_RESULT_UNIT) like '%cm%' then oc.OBSCLIN_RESULT_NUM/100
                else oc.OBSCLIN_RESULT_NUM/39.37 end
    FROM T2DM_PT r
    JOIN DEIDENTIFIED_PCORNET_CDM.CDM.DEID_OBS_CLIN oc 
    ON r.patid = oc.patid AND
        oc.OBSCLIN_TYPE = 'LC' and oc.OBSCLIN_CODE = '8302-2'
    UNION
    -- weight (kg)--
    SELECT r.patid,
            b.measure_date::date,
            round(datediff(day,r.cd_date1,b.measure_date::date)/365.25),
            'WT',b.wt/2.205 -- default at 'lb'
    FROM T2DM_PT r
    JOIN DEIDENTIFIED_PCORNET_CDM.CDM.DEID_VITAL b 
    ON r.patid = b.patid
    WHERE b.wt is not null
    UNION
    select r.patid,
            oc.OBSCLIN_START_DATE::date,
            round(datediff(day,r.cd_date1,oc.OBSCLIN_START_DATE::date)/365.25),'WT',
            case when lower(oc.OBSCLIN_RESULT_UNIT) like 'g%' then oc.OBSCLIN_RESULT_NUM/1000
                when lower(oc.OBSCLIN_RESULT_UNIT) like '%kg%' then oc.OBSCLIN_RESULT_NUM
                else oc.OBSCLIN_RESULT_NUM/2.205 end
    FROM T2DM_PT r
    JOIN DEIDENTIFIED_PCORNET_CDM.CDM.DEID_OBS_CLIN oc 
    ON r.patid = oc.patid AND
        oc.OBSCLIN_TYPE = 'LC' and oc.OBSCLIN_CODE = '29463-7'
    UNION
    -- bmi (kg/m2)--
    SELECT r.patid,
            b.measure_date::date,
            round(datediff(day,r.cd_date1,b.measure_date::date)/365.25),
            'BMI',b.ORIGINAL_BMI
    FROM T2DM_PT r
    JOIN DEIDENTIFIED_PCORNET_CDM.CDM.DEID_VITAL b 
    ON r.patid = b.patid
    WHERE b.ORIGINAL_BMI is not null
    UNION
    select r.patid,
            oc.OBSCLIN_START_DATE::date,
            round(datediff(day,r.cd_date1,oc.OBSCLIN_START_DATE::date)/365.25),
            'BMI',oc.OBSCLIN_RESULT_NUM 
    FROM T2DM_PT r
    JOIN DEIDENTIFIED_PCORNET_CDM.CDM.DEID_OBS_CLIN oc 
    ON r.patid = oc.patid AND
        oc.OBSCLIN_TYPE = 'LC' and oc.OBSCLIN_CODE = '39156-5'
)
,daily_agg as (
    select patid,measure_date,HT,WT,days_since_index,
           case when BMI>100 then NULL else BMI end as BMI,
           case when HT = 0 or WT = 0 or round(WT/(HT*HT))>100 then NULL
                else round(WT/(HT*HT)) 
           end as BMI_CALCULATED
    from (
        select patid,
               measure_type, 
               measure_date, 
               days_since_index, 
               median(measure_num) as measure_num
        from bmi_stk
        group by patid, measure_type, measure_date ,days_since_index
    ) 
    pivot(
        median(measure_num) 
        for measure_type in ('HT','WT','BMI')
    ) as p(patid,measure_date,days_since_index,HT,WT,BMI)
    where (WT is not null and HT is not null and WT>0 and HT>0) or
          (BMI is not null and BMI > 0)
)
,bmi_ordered as (
    select patid,
        measure_date,
        days_since_index,
        round(ht,2) as ht,
        round(wt,2) as wt,
        NVL(bmi_calculated,bmi) as bmi,
        row_number() over (partition by patid order by abs(days_since_index)) as rn
    from daily_agg
    where NVL(BMI,BMI_CALCULATED) is not null and NVL(BMI,BMI_CALCULATED)>0
)
select a.patid, b.ht, b.wt, b.bmi, 
       case when b.bmi < 18.5 then 'underwt'
            when b.bmi >= 18.5 and b.bmi < 25 then 'normal'
            when b.bmi >= 25 and b.bmi < 30 then 'overwt'
            when b.bmi >= 30 and b.bmi < 35 then 'obeseI'
            when b.bmi >= 35 and b.bmi < 40 then 'obeseII'
            when b.bmi >= 40 then 'obeseIII'
            else 'NI'
       end as bmi_class
from T2DM_PT a
left join bmi_ordered b 
on a.patid = b.patid and b.rn = 1
;

select count(distinct patid), count(*) from cov_bmi;

create or replace table cov_bp as 
with multi_cte as (
    select * from
    (
        select   distinct
                 r.PATID
                ,v.SYSTOLIC
                ,v.DIASTOLIC
                ,v.MEASURE_DATE
            from T2DM_PT r 
            join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_VITAL v on r.patid = v.patid
            where v.SYSTOLIC is not null and v.MEASURE_DATE <= r.cd_date1
    )
    unpivot (
    VITAL_VAL for VITAL_TYPE in (SYSTOLIC, DIASTOLIC)
    )
    union all
    -- SBP from OBS_CLIN table
    select   distinct 
             r.PATID
            ,os.OBSCLIN_START_DATE
            ,'SYSTOLIC' as VITAL_TYPE
            ,os.OBSCLIN_RESULT_NUM as VITAL_VAL
        from T2DM_PT r
        join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_OBS_CLIN os on r.patid = os.patid
        where
            -- os.OBSCLIN_TYPE = 'LC' and 
            os.OBSCLIN_CODE in ( '8460-8' --standing
                                ,'8459-0' --sitting
                                ,'8461-6' --supine
                                ,'8479-8' --palpation
                                ,'8480-6' --general
                                )
    union all
    -- DBP from OBS_CLIN table
    select   distinct 
                r.PATID
            ,os.OBSCLIN_START_DATE
            ,'DIASTOLIC' as VITAL_TYPE
            ,os.OBSCLIN_RESULT_NUM as VITAL_VAL
        from T2DM_PT r
        join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_OBS_CLIN os on r.patid = os.patid
        where
            -- os.OBSCLIN_TYPE = 'LC' and 
            os.OBSCLIN_CODE in ( '8454-1' --standing
                                ,'8453-3' --sitting
                                ,'8455-8' --supine
                                ,'8462-4' --general
                                )
)
, bp_ordered as (
    select PATID, SBP, DBP, MEASURE_DATE,
           row_number() over (partition by patid order by MEASURE_DATE desc) as rn
    from multi_cte
    pivot 
    (  
        max(VITAL_VAL) for VITAL_TYPE in ('SYSTOLIC','DIASTOLIC')
    )
    as p(PATID, MEASURE_DATE,SBP, DBP)
)
select a.patid, b.sbp, b.dbp 
from T2DM_PT a
left join bp_ordered b 
on a.patid = b.patid and b.rn = 1
;

select count(distinct patid), count(*) from cov_bp;


create or replace table cov_cci_long as 
select  distinct
        a.PATID
        ,datediff(day,a.cd_date1,NVL(d.DX_DATE::date,d.ADMIT_DATE::date)) as DAYS_SINCE_INDEX
        ,d.DX
        ,d.PDX
        ,d.DX_DATE
        ,d.ADMIT_DATE
        ,d.ENC_TYPE
        ,cci.code_grp as cci_grp
        ,cci.score as cci_score
from T2DM_PT a
join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_DIAGNOSIS d 
on a.PATID = d.PATID
join Z_REF_CCI cci
on d.dx like cci.code||'%' and d.dx_type = cci.code_type
where NVL(d.DX_DATE::date,d.ADMIT_DATE::date)<=a.cd_date1
;



create or replace table cov_cci as 
with cci_uni as (
    select patid, cci_grp, cci_score
    from (
        select a.*, row_number() over (partition by a.patid, a.cci_grp order by a.days_since_index desc) rn
        from cov_cci_long a
    )
    where rn = 1
)
, cci_tot as (
    select patid, sum(cci_score) as cci_total
    from cci_uni
    group by patid
)
, cci_pvt as (
    select * from (
    select patid, cci_grp, 1 as ind from cci_uni
)
pivot (
    max(ind) for cci_grp in (
        'dementia',
        'diab',
        'metacanc',
        'pud',
        'hp',
        'canc',
        'diabwc',
        'cevd',
        'rheumd',
        'aids',
        'mi',
        'msld',
        'chf',
        'pvd',
        'mld',
        'cpd',
        'rend'
    )
    DEFAULT ON NULL (0)
)
as p(patid,dementia,diab,metacanc,pud,hp,canc,diabwc,cevd,rheumd,aids,mi,msld,chf,pvd,mld,cpd,rend)
)
select  distinct a.patid,
        coalesce(b.dementia,0) as cci_dementia,
        coalesce(b.diab,0) as cci_diab,
        coalesce(b.metacanc,0) as cci_metacanc,
        coalesce(b.pud,0) as cci_pud,
        coalesce(b.hp,0) as cci_hp,
        coalesce(b.canc,0) as cci_canc,
        coalesce(b.diabwc,0) as cci_diabwc,
        coalesce(b.cevd,0) as cci_cevd,
        coalesce(b.rheumd,0) as cci_rheumd,
        coalesce(b.aids,0) as cci_aids,
        coalesce(b.mi,0) as cci_mi,
        coalesce(b.msld,0) as cci_msld,
        coalesce(b.chf,0) as cci_chf,
        coalesce(b.pvd,0) as cci_pvd,
        coalesce(b.mld,0) as cci_mld,
        coalesce(b.cpd,0) as cci_cpd,
        coalesce(b.rend,0) as cci_rend,
        coalesce(tot.cci_total,0) as cci_total,
        case when tot.cci_total between 1 and 2 then 'cci_grp1'
             when tot.cci_total between 3 and 4 then 'cci_grp2'
             when tot.cci_total >= 5 then 'cci_grp3'
             else 'cci_grp0'
        end as cci_total_grp
from T2DM_PT a 
left join cci_pvt b on a.patid = b.patid 
left join cci_tot tot on a.patid = tot.patid 
;

select count(*), count(distinct patid) from cov_cci;

create or replace table cov_labs_long as 
select distinct
     a.PATID
    ,coalesce(b.specimen_date, b.lab_order_date, b.result_date) as OBS_DATE
    ,datediff(day,a.cd_date1,coalesce(b.specimen_date, b.lab_order_date, b.result_date)) as DAYS_SINCE_INDEX
    ,b.lab_loinc as OBS_CODE
    ,coalesce(NULLIF(trim(lower(b.raw_lab_name)),''),lower(c.component)) as OBS_NAME
    ,coalesce(NULLIF(lower(b.specimen_source),''),lower(c.system)) as OBS_SRC
    ,b.result_num as OBS_NUM
    ,b.result_unit as OBS_UNIT
    ,b.norm_range_low as OBS_REF_LOW
    ,b.norm_range_high as OBS_REF_HIGH
    ,b.result_qual as OBS_QUAL
    ,b.lab_px
    ,b.lab_px_type
    from T2DM_PT a
    join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_LAB_RESULT_CM b
    on a.patid = b.patid
    left join ONTOLOGY.LOINC.LOINC_V2_17 c
    on b.lab_loinc = c.loinc_num
;

create or replace table cov_labs as
with cr as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where a.obs_code in ('2160-0')
        --   and a.obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and a.obs_num is not null
), bun as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('3094-0')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), egfr as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('98979-8','48642-3','77147-7','48643-1','33914-3','88294-4','88293-6')
        --   and obs_unit = 'mL/min'
          and a.days_since_index between -731 and 0 and obs_num is not null
), egfr2 as (
    select distinct a.patid, coalesce(egfr.days_since_index,cr.days_since_index) as days_since_index,
           case when a.sex = 'M' then coalesce(egfr.obs_num,round(142*power(least(cr.obs_num/0.9,1),-0.302)*power(greatest(cr.obs_num/0.9,1),-1.2)*power(0.9938,a.age_at_index)*1))
                else coalesce(egfr.obs_num,round(142*power(least(cr.obs_num/0.7,1),-0.241)*power(greatest(cr.obs_num/0.7,1),-1.2)*power(0.9938,a.age_at_index)*1.012))
           end as lab_egfr2,
           row_number() over (partition by a.patid order by coalesce(egfr.days_since_index,cr.days_since_index) desc) as rn,
           count(distinct coalesce(egfr.days_since_index,cr.days_since_index)) over (partition by a.patid) as egfr_cnt
    from T2DM_PT_DEMO a 
    left join cr on a.patid = cr.patid
    left join egfr on a.patid = egfr.patid
    where coalesce(egfr.days_since_index,cr.days_since_index) is not null
), pot as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2823-3','6298-4')
        --   and obs_unit = 'mmol/L'
          and a.days_since_index between -731 and 0 and obs_num is not null
), sod as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2951-2','2947-0')
        --   and obs_unit = 'mmol/L'
          and a.days_since_index between -731 and 0 and obs_num is not null
), uralbcr as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('9318-7','14959-1','14958-3')
        --   and obs_unit = 'mmol/L'
          and a.days_since_index between -731 and 0 and obs_num is not null
), uralb as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('14957-5','1754-1','13992-3','29946-1','30003-8','13992-3')
        --   and obs_unit = 'mmol/L'
          and a.days_since_index between -731 and 0 and obs_num is not null
), urcr as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2161-8','20624-3','14683-7','2162-6')
        --   and obs_unit = 'mmol/L'
          and a.days_since_index between -731 and 0 and obs_num is not null
), uralbcr2 as (
    select a.patid, coalesce(uralbcr.days_since_index,least(uralb.days_since_index,urcr.days_since_index)) as days_since_index,
           coalesce(uralbcr.obs_num, round(uralb.obs_num/urcr.obs_num*1000)) as lab_uralbcr2,
           row_number() over (partition by a.patid order by coalesce(uralbcr.days_since_index,least(uralb.days_since_index,urcr.days_since_index)) desc) as rn,
           count(distinct coalesce(uralbcr.days_since_index,least(uralb.days_since_index,urcr.days_since_index))) over (partition by a.patid) as uralbcr_cnt
    from T2DM_PT a 
    left join uralbcr on a.patid = uralbcr.patid
    left join uralb on a.patid = uralb.patid
    left join urcr on a.patid = urcr.patid
    where coalesce(uralbcr.days_since_index,least(uralb.days_since_index,urcr.days_since_index)) is not null
), cal as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('17861-6')
          and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), alb as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('13980-8','2862-1','61152-5','1751-7')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), chol as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2093-3')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), ldl as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2089-1','13457-7','2091-7')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), hdl as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2085-9')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), trig as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('2571-8')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), ast as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('1920-8','30239-8')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), alp as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('6768-6')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), hem as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('20509-6','718-7')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), hba1c as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('17856-6','4548-4')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), fbg as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('1558-6','10450-5','1554-5','17865-7','35184-1')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), mcv as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('787-2','30428-7')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
), uracid as (
    select a.*, row_number() over (partition by a.patid order by a.days_since_index desc) rn 
    from cov_labs_long a
    where obs_code in ('3086-6')
        --   and obs_unit = 'mg/dL'
          and a.days_since_index between -731 and 0 and obs_num is not null
)
select distinct a.patid,
       hba1c.obs_num as hba1c,
       fbg.obs_num as fbg,
       cr.obs_num as scr,
       coalesce(egfr.obs_num, egfr2.lab_egfr2) as egfr,
       bun.obs_num as bun,
       coalesce(uralbcr.obs_num,uralbcr2.lab_uralbcr2) as uacr,
       ldl.obs_num as ldl,
       hdl.obs_num as hdl,
       trig.obs_num as trig,
       chol.obs_num as chol_tot,
       sod.obs_num as sodium,
       pot.obs_num as potassium,
       alb.obs_num as albumin,
       alp.obs_num as alp,
       ast.obs_num as ast,
       hem.obs_num as hemoglobin,
       cal.obs_num as calcium,
       mcv.obs_num as mcv
from T2DM_PT a 
left join cr on a.patid = cr.patid and cr.rn = 1
left join bun on a.patid = bun.patid and bun.rn = 1
left join egfr on a.patid = egfr.patid and egfr.rn = 1
left join egfr2 on a.patid = egfr2.patid and egfr2.rn = 1
left join pot on a.patid = pot.patid and pot.rn = 1
left join sod on a.patid = sod.patid and sod.rn = 1
left join uralbcr on a.patid = uralbcr.patid and uralbcr.rn = 1
left join uralb on a.patid = uralb.patid and uralb.rn = 1
left join urcr on a.patid = urcr.patid and urcr.rn = 1
left join uralbcr2 on a.patid = uralbcr2.patid and uralbcr2.rn = 1
left join cal on a.patid = cal.patid and cal.rn = 1
left join alb on a.patid = alb.patid and alb.rn = 1
left join chol on a.patid = chol.patid and chol.rn = 1
left join ldl on a.patid = ldl.patid and ldl.rn = 1
left join hdl on a.patid = hdl.patid and hdl.rn = 1
left join trig on a.patid = trig.patid and trig.rn = 1
left join ast on a.patid = ast.patid and ast.rn = 1
left join alp on a.patid = alp.patid and alp.rn = 1
left join hem on a.patid = hem.patid and hem.rn = 1
left join hba1c on a.patid = hba1c.patid and hba1c.rn = 1
left join fbg on a.patid = fbg.patid and fbg.rn = 1
left join mcv on a.patid = mcv.patid and mcv.rn = 1
;

create or replace table cov_rx as 
with metformin as (
    select distinct PATID, 1 as ind 
    from T2DM_LONG 
    where PHE_TYPE = 'BIGU'
), tzd as (
    select distinct PATID, 1 as ind 
    from T2DM_LONG 
    where PHE_TYPE = 'TZD'
), sulf as (
    select distinct PATID, 1 as ind 
    from T2DM_LONG 
    where PHE_TYPE = 'SU'
), dpp4 as (
    select distinct PATID, 1 as ind 
    from T2DM_LONG 
    where PHE_TYPE = 'DPP4'
), glp1 as (
    select distinct PATID, 1 as ind 
    from T2DM_LONG 
    where PHE_TYPE = 'GLP1'
), insulin as (
    select distinct PATID, 1 as ind 
    from T2DM_LONG 
    where PHE_TYPE = 'INS'
)
select a.PATID, 
       coalesce(metformin.ind, 0) as metformin_use, 
       coalesce(tzd.ind, 0) as tzd_use,
       coalesce(sulf.ind, 0) as sulfonylurea_use,
       coalesce(dpp4.ind, 0) as dpp4_use,
       coalesce(glp1.ind, 0) as glp1_use,
       coalesce(insulin.ind, 0) as insulin_use
from T2DM_PT a 
left join metformin on metformin.patid = a.patid 
left join tzd on tzd.patid = a.patid 
left join sulf on sulf.patid = a.patid 
left join dpp4 on dpp4.patid = a.patid 
left join glp1 on glp1.patid = a.patid 
left join insulin on insulin.patid = a.patid 
;

select count(*), count(distinct patid) from cov_rx;

create or replace table cov_vis_long as 
select distinct
     r.PATID
    ,enc.ENC_TYPE
    ,enc.ADMIT_DATE
    ,enc.DISCHARGE_DATE
    ,enc.DISCHARGE_STATUS
    ,enc.DISCHARGE_DISPOSITION
    ,enc.DRG
    ,enc.FACILITYID
    ,enc.FACILITY_LOCATION
    ,enc.FACILITY_TYPE
    ,enc.PAYER_TYPE_PRIMARY
    ,case when enc.PAYER_TYPE_PRIMARY like '1%' then 'medicare'
            when enc.PAYER_TYPE_PRIMARY like '5%' then 'commercial'
            when enc.PAYER_TYPE_PRIMARY like '82%' then 'selfpay'
            when enc.PAYER_TYPE_PRIMARY is NULL or trim(enc.PAYER_TYPE_PRIMARY) = '' or enc.PAYER_TYPE_PRIMARY in ('NI','UN') then 'NI'
        end as PAYER_TYPE_PRIMARY_GRP
    ,enc.RAW_PAYER_TYPE_PRIMARY
    ,enc.RAW_PAYER_ID_PRIMARY   
    ,enc.PROVIDERID
    ,prov.PROVIDER_SPECIALTY_PRIMARY
    ,prov.PROVIDER_NPI
    ,prov.RAW_PROVIDER_SPECIALTY_PRIMARY
    -- ,prov.RAW_PROV_NAME
    -- ,prov.RAW_PROV_TYPE            
    ,datediff(day,r.cd_date1,enc.admit_date) as DAYS_SINCE_INDEX
from T2DM_PT r 
join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_ENCOUNTER enc on r.patid = enc.patid
left join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_PROVIDER prov on enc.providerid = prov.providerid
where enc.admit_date < '2025-10-01'
;

create or replace table cov_vis as 
with av as (
    select patid, count(distinct admit_date) as vis_cnt 
    from cov_vis_long
    where days_since_index between -730 and -1 and ENC_TYPE = 'AV'
    group by patid
), th as (
    select patid, count(distinct admit_date) as vis_cnt 
    from cov_vis_long
    where days_since_index between -730 and -1 and ENC_TYPE = 'TH'
    group by patid
), ed as (
    select patid, count(distinct admit_date) as vis_cnt 
    from cov_vis_long
    where days_since_index between -730 and -1 and ENC_TYPE in ('ED','EI')
    group by patid
), ip as (
    select patid, count(distinct admit_date) as vis_cnt, sum(datediff('day',admit_date,discharge_date)) as los
    from cov_vis_long
    where days_since_index between -730 and -1 and ENC_TYPE in ('IP','EI')
    group by patid
), payer as (
    select patid, payer_type_primary_grp from 
    (
        select a.*, row_number() over (partition by a.patid order by abs(a.days_since_index)) rn
        from cov_vis_long a
        where a.enc_type = 'AV' and payer_type_primary_grp <> 'NI'
    )
    where rn = 1
)
select distinct a.patid,
       coalesce(av.vis_cnt, 0) as av_cnt,
       coalesce(th.vis_cnt, 0) as th_cnt,
       coalesce(ed.vis_cnt, 0) as ed_cnt,
       coalesce(ip.vis_cnt, 0) as ip_cnt,
       coalesce(ip.los, 0) as ip_los,
       coalesce(payer.payer_type_primary_grp,'NI') as payor_type
from T2DM_PT a 
left join av on a.patid = av.patid 
left join th on a.patid = th.patid 
left join ed on a.patid = ed.patid 
left join ip on a.patid = ip.patid 
left join payer on a.patid = payer.patid
;

select count(*), count(distinct patid) from cov_vis;

create or replace table cov_window as 
select a.patid, 
     max(coalesce(b.discharge_date::date,b.admit_date::date)) as censor_date,
     datediff('days',min(coalesce(b.discharge_date,b.admit_date)),a.cd_date1) as baseline_coc
from T2DM_PT a 
join cov_vis_long b
group by a.patid,a.cd_date1
;

select count(*), count(distinct patid) from cov_window;

create or replace table cov_death as 
with dth_ordered as (
    select a.patid, b.death_date::date as death_date, 
           row_number() over (partition by a.patid order by b.death_source) as rn
    from T2DM_PT a 
    join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_DEATH b 
    on a.patid = b.patid
) 
select patid, death_date 
from dth_ordered
where rn = 1
;
select count(*), count(distinct patid) from cov_death;

create or replace table cov_sdh as  
with ruca_ordered as (
    select patid, ruca, days_since_index,
           row_number() over (partition by patid order by abs(days_since_index)) as rn
    from (
        select a.patid, 
               datediff('day',a.cd_date1,coalesce(b.address_period_end,b.address_period_start)) as days_since_index,
               b.ruca
    from T2DM_PT a 
    join DEIDENTIFIED_PCORNET_CDM.CDM.DEID_LDS_ADDRESS_HISTORY b 
    on a.patid = b.patid
    )
)
select a.patid, 
       coalesce(b.ruca, 'NI') as ruca 
from T2DM_PT a  
left join ruca_ordered b 
on a.patid = b.patid and b.rn = 1
;

select count(distinct patid), count(*) from cov_sdh;

create or replace table T2DM_ASET as 
select a.*
       ,cov_smk.* exclude (PATID)
       ,cov_bmi.* exclude(PATID)
       ,cov_bp.* exclude(PATID)
       ,cov_cci.* exclude (PATID)
       ,cov_labs.* exclude (PATID)
       ,cov_rx.* exclude (PATID)
       ,cov_vis.* exclude (PATID)
       ,cov_window.* exclude (PATID)
       ,cov_sdh.* exclude (PATID)
       ,cov_death.* exclude(PATID)
from T2DM_PT_DEMO a 
join cov_smk on a.patid = cov_smk.patid
join cov_bp on a.patid = cov_bp.patid 
join cov_bmi on a.patid = cov_bmi.patid
join cov_cci on a.patid = cov_cci.patid 
join cov_labs on a.patid = cov_labs.patid 
join cov_rx on a.patid = cov_rx.patid 
join cov_vis on a.patid = cov_vis.patid
join cov_window on a.patid = cov_window.patid 
join cov_sdh on a.patid = cov_sdh.patid
left join cov_death on a.patid = cov_death.patid
;

select count(*), count(distinct patid) from T2DM_ASET;
-- 52446

select * from T2DM_ASET limit 5;