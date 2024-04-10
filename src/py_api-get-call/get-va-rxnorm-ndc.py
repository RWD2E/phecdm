import os
import api_get_rxnav as apirxnav
import pandas as pd

path_to_kb = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# unit test - single search
rxnav_cls = apirxnav.RxNavSearch()
print(rxnav_cls.get_rxcui_from_va("HS500"))

# https://www.va.gov/formularyadvisor/ 

# apirxnav.batch_write_rx_code_json(
#     path_to_save = path_to_kb, # save to computational phenotype kb
#     filename_to_save = 'osa-cov-rx-rxcui',
#     sterms = [
#         'CV100', # beta blockers/related
#         'CV150', # alpha blockers/related
#         'CV200', # calcium channel blockers
#         'CV400', # antihypertensive combinations
#         'CV490', # antihypertensive, others
#         'CV701', # thiazides/related diuretics
#         'CV702', # loop diuretics
#         'CV703', # carbonic anhydrase inhibitor diuretics
#         'CV704', # potassium sparing/combinations diretics
#         'CV709', # diuretics, other
#         'CV800', # ACE inhibitors
#         'CV805', # angiotensin II inhibitor
#         'CV806', # direct renin inhibitor
#         'CV350', # antilipemic agent
#         'BL110', # anticoagulants
#         'HS500'  # blood glucose regulation agent
#     ],
#     sterm_type = 'va',
#     verbose=True
# )


# apirxnav.batch_write_rx_code_json(
#     path_to_save = path_to_kb, # save to computational phenotype kb
#     filename_to_save = 'osa-cov-rx-rxcui',
#     sterms = [
#         'CV100', # beta blockers/related
#         'CV150', # alpha blockers/related
#         'CV200', # calcium channel blockers
#         'CV400', # antihypertensive combinations
#         'CV490', # antihypertensive, others
#         'CV701', # thiazides/related diuretics
#         'CV702', # loop diuretics
#         'CV703', # carbonic anhydrase inhibitor diuretics
#         'CV704', # potassium sparing/combinations diretics
#         'CV709', # diuretics, other
#         'CV800', # ACE inhibitors
#         'CV805', # angiotensin II inhibitor
#         'CV806', # direct renin inhibitor
#         'CV350', # antilipemic agent
#         'BL110', # anticoagulants
#         'HS500'  # blood glucose regulation agent
#     ],
#     sterm_type = 'va',
#     verbose=True
# )