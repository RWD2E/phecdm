import json
import pandas as pd

cdtype_mapping = {
    'icd9-cm':'09',
    'icd9-px':'09',
    'icd10-cm':'10',
    'icd10-pcs':'10',
    'loinc':'LC',
    'rxnorm':'RX',
    'ndc':'ND',
    'snomed':'SM',
    'hcpcs':'CH',
    'cpt':'CH'
}

def vs_json_to_csv(
    path_to_json,
    path_to_save
):
    '''
    function to transfer standardized valueset file in json to csv
    input json structure: 
    {'acronym of disease phenotype':{
        "code-type-1":[],
        "code-type-2":[].
        "meta":{
            "full":"long name of disease phenotype,
            ...
        }
    }
    '''
    # read json file
    with open(path_to_json,'r') as json_file:
        json_dict = json.load(json_file)

    # parse
    df_meta_lst = []
    df_code_lst = []
    for key,val in json_dict.items():
        for subkey, subval in val.items():
            if subkey == 'meta':
                # integrate meta
                df_meta = pd.DataFrame({k:[v] for k,v in subval.items()})
                df_meta['CODE_GRP'] = key
                df_meta_lst.append(df_meta)     
            else:
                # integrate codes
                df_code = pd.DataFrame(
                    {
                        'CODE_TYPE':[subkey]*len(subval),
                        'CODE':subval
                    }
                )
                df_code['CODE_GRP'] = key
                df_code = df_code.replace(cdtype_mapping)
                df_code_lst.append(df_code)

    # stack and save
    df_meta_stk = pd.concat(df_meta_lst, axis=0, ignore_index=True).drop_duplicates()
    df_code_stk = pd.concat(df_code_lst, axis=0, ignore_index=True).drop_duplicates()
    df = df_meta_stk.merge(df_code_stk, on='CODE_GRP', how='inner')
    df.to_csv(path_to_save,index = False,quoting=1)