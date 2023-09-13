import os
import pandas as pd
import json

path_to_kb = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

OVERWRITE_EXISTING = True

dir_path = 'C:/repos/GROUSE/'
src_file = pd.read_csv(f"{dir_path}/ref/raw/pde-ndc-raw.csv")
src_file['NDC'] = src_file['NDC'].astype(str).str.zfill(11)

# merge with source ndc list and extract standardized info on strength and unit
with open(f"{path_to_kb}/ndc-rxcui-collapse.json", 'r') as json_file:
    ref_file = json.load(json_file)
    ref_file_df = pd.DataFrame(ref_file)
    str_dose_unit = src_file.merge(
        ref_file_df, 
        left_on='NDC', right_on = "ndc",
        how='left'
    )
    str_dose_unit = str_dose_unit.drop(columns=['ndc','packaging','str','dose-unit'])
    str_dose_unit.drop_duplicates(keep=False,inplace=True,subset=['NDC']) 

    # save aside unmatched records for another round of matching or manual review
    str_dose_unit_um = str_dose_unit[str_dose_unit['dose'].isna()]
    str_dose_unit_um = str_dose_unit_um.drop(columns=['rxcui','dose','unit','in'])
    str_dose_unit_um.to_csv(f"{dir_path}/ref/raw/pde-ndc-raw-new.csv", index=False, mode='w')
    print(f"number of unmatched items: {str_dose_unit_um.shape[0]}")

    # for rows with standardized dose-unit match, concatenate component strigs for drug pack
    str_dose_unit = str_dose_unit.dropna(subset=['dose'])
    col_to_concat = ['dose','unit','in']
    def cond_concat(lst):
        if not lst:
            return ''
        elif len(lst) ==1:
            return lst[0]
        else:
            return ';'.join(lst)
    str_dose_unit[col_to_concat] = str_dose_unit[col_to_concat].apply(lambda x: x.apply(cond_concat))

    # write or append to current mapping
    path_to_map = f"{dir_path}/ref/STR2DOSEUNIT.csv"
    try:
        os.path.exists(path_to_map)
        if OVERWRITE_EXISTING:
            str_dose_unit.to_csv(path_to_map, index=False, mode='w')
        else:
            str_dose_unit.to_csv(path_to_map, index=False, mode='a', header=False)
    except:
        print(f"file {path_to_map} doesn't exist.")
