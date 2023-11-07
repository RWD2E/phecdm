import os
import api_get_rxnav as apirxnav
import pandas as pd

path_to_kb = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# unit test - single search
# rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_rxcui_from_va("CV400"))

# https://www.va.gov/formularyadvisor/ 

apirxnav.batch_write_rx_code_json(
    path_to_save = path_to_kb, # save to computational phenotype kb
    filename_to_save = 'osa-cov-rx-rxcui',
    sterms = [
        'CV400', # antihypertensive combinations
        'CV490', # antihypertensive, others
        'CV350', # antilipemic agent
        'BL110', # anticoagulants
        'HS500'  # blood glucose regulation agent
    ],
    sterm_type = 'va',
    verbose=True
)
