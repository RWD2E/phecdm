
import pandas as pd
import json
import urllib.request as urlreq


def sqlgen_phe_spark(
    src_json_url,      # url where source phenotype mapping can be found, e.g. https://raw.githubusercontent.com/RWD2E/phecdm/main/res/valueset_curated/vs-mmm.json
    which_phenotype,   # specify codeset for which phenotype
    cd_field_map,      # actual code field mapping
    cdtype_field_map,  # code type field mapping
    cdtype_value_map,  # code type valueset mapping
    alias=''           # if an alias , especially embeded in a "join" statement
):
    '''
    sql where clause for cohort selection based on ICD code list
    '''
    # load json file from source
    with urlreq.urlopen(src_json_url) as url:
        phemap = json.loads(url.read().decode())

    # loop over code types
    sql_str_lst = []
    for cdt in phemap[which_phenotype]:
        for prec,cdlst in phemap[which_phenotype][cdt].items():
            sql_str = ''
            if not cdlst: continue
            # codetype
            cdtype_quote = []
            for type in cdtype_value_map[cdt]:
                cdtype_quote.append("'"+ type +"'")
            cdtype_quote_str = ",".join(cdtype_quote)
            sql_str += alias + cdtype_field_map[cdt] + " in (" + cdtype_quote_str + ") AND "
            # expand range
            if prec == "range":
                for rg in cdlst: 
                    rg_pos = rg.splint('-') 
                    cdlst_new = range(rg_pos[0],rg_pos[1]+1)
                cdlst = cdlst_new
            # construct code list string
            cd_quote = []
            for code in cdlst:
                cd_quote.append("'"+ code +"'")
            cd_quote_str = ",".join(cd_quote)
            # complete search sentence
            if prec == 'lev0':
                sql_str += "substring_index(upper("+ alias + cd_field_map[cdt] +"),'.',1) in (" + cd_quote_str +")" 
            elif prec == 'lev1':
                str_len = len(cdlst[0])
                sql_str += "substring(upper("+ alias + cd_field_map[cdt] +"),1,"+ str_len+1 +") in (" + cd_quote_str +")" 
            else: # lev2, range, exact
                sql_str += "upper("+ alias + cd_field_map[cdt] +") in (" + cd_quote_str +")" 
            sql_str_lst.append(sql_str)

    # concatenate them together
    sql_str_master = "(" + ") OR (".join(sql_str_lst) + ")"
    return(sql_str_master)

cd_field_map = {
    'icd9-cm':'conditioncode.standard.id',
    'icd10-cm':'conditioncode.standard.id',
    'hcpcs':'procedurecode.standard.id',
    'drg':'conditioncode.standard.id'
}
cdtype_field_map = {
    'icd9-cm':'conditioncode.condingSystemId',
    'icd10-cm':'conditioncode.condingSystemId',
    'hcpcs':'procedurecode.condingSystemId',
    'drg':'conditioncode.condingSystemId'
}
cdtype_value_map = {
    'icd9-cm':['2.16.840.1.113883.6.103'],
    'icd10-cm':['2.16.840.1.113883.6.4'],
    'hcpcs':['2.16.840.1.113883.6.14'],
    'drg':['urn:cerner:codingsystem:drg:aprdrg','urn:cerner:codingsystem:drg:apdrg']
}

test = sqlgen_phe_spark(
    src_json_url = 'https://raw.githubusercontent.com/RWD2E/phecdm/main/res/valueset_curated/vs-mmm.json',
    which_phenotype = 'delivery-vaginal',
    cd_field_map = cd_field_map,
    cdtype_field_map = cdtype_field_map,
    cdtype_value_map = cdtype_value_map
)

print(test)