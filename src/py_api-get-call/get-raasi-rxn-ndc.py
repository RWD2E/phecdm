import os
import api_get_rxnav as apirxnav
import pandas as pd
import json

path_to_tgt = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
            )
        ),
    'res','valueset_autogen'
)

##--- test single case
# rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_ndc_from_rxcui('1991302'))
# print(rxnav_cls.get_rxcui_from_str('semaglutide'))

##--- load source generic names
src_file = pd.read_csv(f"{path_to_tgt}/rx-ref-raasi_input.csv")

##--- api call to get output json file
# apirxnav.batch_write_rx_code_json(
#     path_to_save = path_to_tgt, #absolute path,
#     filename_to_save = 'rx-ref-raasi_output',
#     sterms = src_file['IN'],
#     sterm_type = 'string',
#     verbose=True
# )

# from standardized json file to 4-columnar reference table
with open(f"{path_to_tgt}/rx-ref-raasi_output.json",'r') as json_file:
    json_lst = json.load(json_file)

df_lst = []
for ing in json_lst:
    for k in json_lst[ing]:
        df = pd.DataFrame({
            'IN':[ing],
            'RXCUI':[k['rxcui']],
            'NAME':[k['name']],
            'TTY':[k['tty']],
            'NDC':[k['ndc']]
        })
        df_lst.append(df)
df_stk = pd.concat(df_lst, axis=0, ignore_index=True)
df_stk_span = df_stk.explode('NDC')
df_merge = pd.merge(src_file,df_stk_span,on='IN')
df_merge.to_csv(f"{path_to_tgt}/rx-ref-raasi_rxcui-ndc.csv",index = False)

# manually move to ./ref folder after review