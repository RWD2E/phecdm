import os
import api_get_rxnav as apirxnav
import pandas as pd

path_to_kb = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# validation - single search
# rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_ndc_details("64597030113",expand=False))
# print(rxnav_cls.get_ndc_details("64597030113",expand=True))

dir_path = 'C:/repos/cdc_als4m/'
src_file = pd.read_csv(f"{dir_path}/ref/all_ndc_raw.csv")
src_file['NDC'] = src_file['NDC'].astype(str).str.replace('N','') # prefix N to avoid removal of leading 0s

apirxnav.batch_write_ndc_details_json(
    path_to_save = path_to_kb, # save to computational phenotype kb
    filename_to_save = 'als-all-rx-ndc',
    sterms = src_file['NDC'],
    expand = False,
    verbose = True,
    overwrite = True
)
