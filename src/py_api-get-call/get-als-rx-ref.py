import pandas as pd
import json

with open('C:/repos/PheCDM/res/valueset_autogen/als-all-rx-rxcui.json','r') as json_file:
    json_lst = json.load(json_file)

df_lst = []
for k in json_lst:
    df = pd.DataFrame({
        'RXCUI':[k['rxcui']]*len(k['in']),
        'IN':k['in']
    })
    df_lst.append(df)
df_stk = pd.concat(df_lst, axis=0, ignore_index=True)
df_stk.to_csv(
    'C:/repos/cdc_als4m/ref/als_rxcui_ref.csv',
    index = False
)


with open('C:/repos/PheCDM/res/valueset_autogen/als-all-rx-ndc.json','r') as json_file:
    json_lst = json.load(json_file)

df_lst = []
for k in json_lst:
    if 'in' in k:
        df = pd.DataFrame({
            'NDC':[k['ndc']]*len(k['in']),
            'IN':k['in']
        })
        df_lst.append(df)
df_stk = pd.concat(df_lst, axis=0, ignore_index=True)
df_stk.to_csv(
    'C:/repos/cdc_als4m/ref/als_ndc_ref.csv',
    index = False
)