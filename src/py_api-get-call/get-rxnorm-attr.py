import os
import api_get_rxnav as apirxnav
import pandas as pd

path_to_kb = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# validation - single search
# rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_rxcui_details("1040058",expand=False))
# print(rxnav_cls.get_rxcui_details("1040058",expand=True))

dir_path = 'C:/repos/cdc_als4m/'
src_file = pd.read_csv(f"{dir_path}/ref/all_rxcui_raw.csv")
src_file['RXNORM_CUI'] = src_file['RXNORM_CUI'].astype(str).str.replace('R','') # prefix R to avoid removal of leading 0s

apirxnav.batch_write_rxcui_details_json(
    path_to_save = path_to_kb, # save to computational phenotype kb
    filename_to_save = 'als-all-rx-rxcui',
    sterms = src_file['RXNORM_CUI'],
    expand = False,
    verbose = True,
    overwrite = True
)
