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

prefix = "rx-ref-aha"
# prefix = "rx-ref-aht"
# prefix = "rx-ref-lld"
# prefix = "rx-ref-atd"

##--- load source generic names
src_file = pd.read_csv(f"{path_to_tgt}/{prefix}_input.csv")

##--- api call to get output json file
# apirxnav.batch_write_rx_code_json(
#     path_to_save = path_to_tgt, #absolute path,
#     filename_to_save = f"{prefix}_output",
#     sterms = src_file['IN'],
#     sterm_type = 'string',
#     verbose=True
# )

# from standardized json file to 5-columnar reference table
# with open(f"{path_to_tgt}/{prefix}_output.json",'r') as json_file:
#     json_lst = json.load(json_file)

# df_lst = []
# for ing in json_lst:
#     for k in json_lst[ing]:
#         df = pd.DataFrame({
#             'ING':[ing],
#             'RXCUI':[k['rxcui']],
#             'NAME':[k['name']],
#             'TTY':[k['tty']],
#             'NDC':[k['ndc']]
#         })
#         df_lst.append(df)
# df_stk = pd.concat(df_lst, axis=0, ignore_index=True)
# df_stk_span = df_stk.explode('NDC')
# df_merge = pd.merge(src_file,df_stk_span,on='IN')
# df_merge.to_csv(f"{path_to_tgt}/{prefix}.csv",index = False)

# manually move to ./ref folder after review

# a subseq table with reference strength and reference units for rxcui codes of TTY = ['SBD','SCD','SBDG','SCDG'] 
with open(f"{path_to_tgt}/{prefix}_output.json",'r') as json_file:
    json_lst = json.load(json_file)

rxn_lst = [
    entry["rxcui"]
    for entries in json_lst.values()
    for entry in entries
    if entry.get("tty") in ("SBD", "SCD" ,"SBDC", "SCDC", "GPCK", "BPCK")
]

apirxnav.batch_write_rxcui_details_json(
    path_to_save = path_to_tgt,
    filename_to_save = f"{prefix}_detail_output",
    sterms = rxn_lst,
    expand = False,
    verbose = True,
    overwrite = True
)

# read json file
with open(f"{path_to_tgt}/{prefix}_detail_output.json",'r') as json_file:
    json_lst = json.load(json_file)

# parse
detail_lst = []
for item in json_lst:
    detail_lst.append({
        "rxcui": item.get("rxcui"),
        "in": ", ".join(item.get("in", [])),
        "str": ", ".join(item.get("str", [])),
        "unit": ", ".join(item.get("unit", []))
    })

# explode
df = pd.DataFrame.from_records(detail_lst)
for col in ["in", "str", "unit"]: 
    df[col] = df[col].str.split(",").apply(lambda lst: [s.strip() for s in lst])
df = df.explode(["in", "str", "unit"], ignore_index=True)

# save
df.to_csv(f"{path_to_tgt}/{prefix}_detail.csv",index = False,quoting=1)
