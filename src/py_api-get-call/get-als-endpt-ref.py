import pandas as pd
import json

# cd type mapping
tty_mapping = {
    'icd9':'09',
    'icd10':'10',
    'hcpcs':'CH'
}

# endpt type mapping
endptty_mapping = {
    'icd9':'DX',
    'icd10':'DX',
    'hcpcs':'PX'
}

# endpt mapping
endpt_mapping = {
    "speech":"bulbar",
    "swallowing":"bulbar",
    "muscle-strength":"limb",
    "gait":"limb",
    "involuntary-muscle-movement":"limb",
    "myopathy":"limb",
    "pain":"limb",
    "other":"limb",
    "mobility":"limb",
    "nutrition-support":"need-peg",
    "respiratory-support":"need-niv"
}

with open('C:/repos/PheCDM/res/valueset_curated/vs-als-staging.json','r') as json_file:
    df = json.load(json_file)

df_lst = []
for k,v in df.items():
    for k2,v2 in v.items():
        df = pd.DataFrame(v2.items(), columns=['Key',"Value"])
        df.rename(columns={'Key': 'CD_TYPE','Value':'CD'}, inplace=True)
        df = df.explode('CD')
        df['ENDPT_SUB'] = k2
        df['ENDPT'] = k
        df_lst.append(df)

df_stk = pd.concat(df_lst, axis=0, ignore_index=True)
df_stk['ENDPT_TYPE'] = df_stk['CD_TYPE'].map(endptty_mapping)
df_stk['ENDPT_GRP'] = df_stk['ENDPT'].map(endpt_mapping)
df_stk['CD_TYPE'] = df_stk['CD_TYPE'].map(tty_mapping)
df_stk['CD'] = df_stk['CD'].str.replace('.', '')

df_stk.to_csv(
    'C:/repos/cdc_als4m/ref/als_endpt_ref.csv',
    index = False
)
