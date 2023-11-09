import pandas as pd
import json
import load_vs_utils as lv

with open('C:/repos/PheCDM/res/valueset_autogen/osa-cov-rx-rxcui.json','r') as json_file:
    json_lst = json.load(json_file)

ndc_lst = []
rxn_lst = []
in_lst = []
for cls in json_lst:
    for cd in json_lst[cls]:
        for subcd in cd["allrelacodes"]:
            rxn_lst.append(
                pd.DataFrame({
                    'VACLS':[cls],
                    'RXNORM':[subcd['rxcui']],
                    'NAME':[subcd['name']],
                    'TTY':[subcd['tty']]
                })
            )
            if subcd["ndc"]:
                ndc_lst.append(
                    pd.DataFrame({
                        'VACLS':[cls]*len(subcd["ndc"]),
                        'RXNORM':[subcd['rxcui']]*len(subcd["ndc"]),
                        'NAME':[subcd['name']]*len(subcd["ndc"]),
                        'NDC':subcd["ndc"]
                    })
                )
            if subcd["tty"] in ('IN','MIN'):
                in_lst.append(
                    pd.DataFrame({
                        'VACLS':[cls],
                        'IN':[subcd["name"]]
                    })
                )

df_stk = pd.concat(rxn_lst, axis=0, ignore_index=True).drop_duplicates()
df_stk.to_csv(
    'C:/repos/gpc-obesity-osa/ref/osa_rx_rxcui_ref.csv',
    index = False
)

df_stk = pd.concat(ndc_lst, axis=0, ignore_index=True).drop_duplicates()
df_stk.to_csv(
    'C:/repos/gpc-obesity-osa/ref/osa_rx_ndc_ref.csv',
    index = False
)

df_stk = pd.concat(in_lst, axis=0, ignore_index=True).drop_duplicates()
df_stk.to_csv(
    'C:/repos/gpc-obesity-osa/ref/osa_rx_in_ref.csv',
    index = False
)

# lv.vs_json_to_csv(
#     path_to_json = 'C:/repos/phecdm/res/valueset_curated/vs-osa-comorb.json',
#     path_to_save = 'C:/repos/gpc-obesity-osa/ref/osa_comorb_ref.csv'
# )

# lv.vs_json_to_csv(
#     path_to_json = 'C:/repos/phecdm/res/valueset_curated/vs-charlson-comorb-index.json',
#     path_to_save = 'C:/repos/gpc-obesity-osa/ref/osa_cci_ref.csv'
# )