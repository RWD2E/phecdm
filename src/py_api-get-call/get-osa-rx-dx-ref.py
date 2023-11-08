import pandas as pd
import json

# with open('C:/repos/PheCDM/res/valueset_autogen/osa-cov-rx-rxcui.json','r') as json_file:
#     json_lst = json.load(json_file)

# ndc_lst = []
# rxn_lst = []
# in_lst = []
# for cls in json_lst:
#     for cd in json_lst[cls]:
#         for subcd in cd["allrelacodes"]:
#             rxn_lst.append(
#                 pd.DataFrame({
#                     'VACLS':[cls],
#                     'RXNORM':[subcd['rxcui']],
#                     'NAME':[subcd['name']],
#                     'TTY':[subcd['tty']]
#                 })
#             )
#             if subcd["ndc"]:
#                 ndc_lst.append(
#                     pd.DataFrame({
#                         'VACLS':[cls]*len(subcd["ndc"]),
#                         'RXNORM':[subcd['rxcui']]*len(subcd["ndc"]),
#                         'NAME':[subcd['name']]*len(subcd["ndc"]),
#                         'NDC':subcd["ndc"]
#                     })
#                 )
#             if subcd["tty"] in ('IN','MIN'):
#                 in_lst.append(
#                     pd.DataFrame({
#                         'VACLS':[cls],
#                         'IN':[subcd["name"]]
#                     })
#                 )

# df_stk = pd.concat(rxn_lst, axis=0, ignore_index=True).drop_duplicates()
# df_stk.to_csv(
#     'C:/repos/gpc-obesity-osa/ref/osa_rx_rxcui_ref.csv',
#     index = False
# )

# df_stk = pd.concat(ndc_lst, axis=0, ignore_index=True).drop_duplicates()
# df_stk.to_csv(
#     'C:/repos/gpc-obesity-osa/ref/osa_rx_ndc_ref.csv',
#     index = False
# )

# df_stk = pd.concat(in_lst, axis=0, ignore_index=True).drop_duplicates()
# df_stk.to_csv(
#     'C:/repos/gpc-obesity-osa/ref/osa_rx_in_ref.csv',
#     index = False
# )

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
                df_code_lst.append(df_code)

    # stack and save
    df_meta_stk = pd.concat(df_meta_lst, axis=0, ignore_index=True).drop_duplicates()
    df_code_stk = pd.concat(df_code_lst, axis=0, ignore_index=True).drop_duplicates()
    df = df_meta_stk.merge(df_code_stk, on='CODE_GRP', how='inner')
    df.to_csv(path_to_save,index = False)

vs_json_to_csv(
    path_to_json = 'C:/repos/phecdm/res/valueset_curated/vs-osa-comorb.json',
    path_to_save = 'C:/repos/gpc-obesity-osa/ref/osa_comorb_ref.csv'
)

vs_json_to_csv(
    path_to_json = 'C:/repos/phecdm/res/valueset_curated/vs-charlson-comorb-index.json',
    path_to_save = 'C:/repos/gpc-obesity-osa/ref/osa_cci_ref.csv'
)