import os
import api_get_rxnav as apirxnav
import pandas as pd

path_to_tgt = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# validation - single fun
rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_rxcui_details("1923432",expand=True))
# print(rxnav_cls.get_ndc_details("50383023310",expand=True))
# print(rxnav_cls.get_ndc_details("50383023310",expand=False))

# prod run
src_dir_loc = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/res/valueset_autogen'
src_file_loc = src_dir_loc + '/pde-ndc-raw.csv'    
src_vs = pd.read_csv(src_file_loc)
src_vs['NDC'] = src_vs['NDC'].astype(str).str.zfill(11)

apirxnav.batch_write_ndc_details_json(
    path_to_save = src_dir_loc, #absolute path,
    filename_to_save = 'pde-ndc-norm-collapse',
    sterms = src_vs['NDC'],
    expand=False,
    verbose=True
)