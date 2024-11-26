
-- https://loinc.org/kb/users-guide/loinc-database-structure/
-- LP are coded representations of the attribute values that combine to create a LOINC term
-- LG is sets of terms that might be considered equivalent for a particular purpose
-- Archetype: The LOINC number of the most general representative term for a specific Group. For example, in a Group rolled up by method, the methodless term is the archetype term

-- use LG to find similar labs? 
select * from ontology.loinc.group_loinc_terms_v2_17
where groupid = 'LG7967-5'
;

-- how to find panel to lab mapping? 
-- use LOINC relational table to group labs? 
select * from ontology.loinc.loinc_v2_17
where loinc_num = '2345-7'
;

/* backtracking, Iterative Deepening Search */
select * from ontology.loinc.multiaxialhierarchy_v2_17
where code = '2345-7'
;
-- LP29693-6.LP343631-0.LP7786-9.LP31399-6.LP14635-4.LP385540-2

-- use LP to find similar labs? 
select * from ontology.loinc.loinc_part_link_primary_v2_17
where partnumber = 'LP14635-4';

-- find all loinc codes for the specific component
select a.* from ontology.loinc.loinc_v2_17 a 
join ontology.loinc.loinc_part_link_primary_v2_17 b 
on a.loinc_num = b.loincnumber
where b.partnumber = 'LP14635-4'
;


select * from ontology.loinc.part_v2_17
where partnumber in (
    'LP29693-6',
    'LP7786-9',
    'LP7834-7',
    'LP14130-6',
    'LP386863-7'
)
;

select * from ontology.loinc.loinc_part_link_primary_v2_17
where partnumber = 'LP14130-6'
;

select * from ontology.loinc.loinc_part_link_supplementary_v2_17
where partnumber = 'LP14130-6'
;

select * from ontology.loinc.part_related_code_mapping_v2_17
where partnumber = 'LP14130-6'
;