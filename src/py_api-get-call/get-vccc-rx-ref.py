import json
import pandas as pd

path_to_json = 'C:/repos/phecdm/res/valueset_autogen/vccc-all-med-rxcui.json'
path_to_save = 'C:/repos/r61-r33-vccc-kumc/ref/med_rxcui_ref.csv'

# read json file
with open(path_to_json,'r') as json_file:
    json_lst = json.load(json_file)

# parse
df_in_lst = []
df_cls_lst = []
for item in json_lst:
    df_in = pd.DataFrame(
        {
            'IN': item['in']
        }
    )
    try:
        df_in['STR'] = item['str']
        df_in['UNIT'] = item['unit']
    except:
        print('Above ingredient.')

    df_in['RXNORM_CUI'] = item['rxcui']
    df_in_lst.append(df_in)

    if 'classes' in item:
        try: 
            df_cls = pd.DataFrame([{
                'VA_CLS':x['className'],
                'VA_CLS_CD':x['classId']
            } for x in item['classes'] if x['classType']=='VA'])
            df_cls['RXNORM_CUI'] = item['rxcui']           
            df_cls_lst.append(df_cls)
        except: 
            print('No VA class.')

# stack and save
df_in_stk = pd.concat(df_in_lst, axis=0, ignore_index=True).drop_duplicates()
df_cls_stk = pd.concat(df_cls_lst, axis=0, ignore_index=True).drop_duplicates()
df = df_in_stk.merge(df_cls_stk, on='RXNORM_CUI', how='outer')
df.to_csv(path_to_save,index = False,quoting=1)