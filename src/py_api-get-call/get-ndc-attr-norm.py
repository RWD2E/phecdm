import os
import api_get_rxnav as apirxnav

path_to_kb = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# validation - single search
rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_rxcui_details("1923432",expand=True))
# print(rxnav_cls.get_ndc_details("50383023310",expand=False))
print(rxnav_cls.get_ndc_details("60258019409",expand=False))
# print(rxnav_cls.get_rxcui_details("656128",expand=True))

# dir_path = 'C:/repos/GROUSE/'
# src_file = pd.read_csv(f"{dir_path}/ref/raw/pde-ndc-raw.csv")
# src_file['NDC'] = src_file['NDC'].astype(str).str.zfill(11)

# apirxnav.batch_write_ndc_details_json(
#     path_to_save = path_to_kb, # save to computational phenotype kb
#     filename_to_save = 'ndc-rxcui-collapse',
#     sterms = src_file['NDC'],
#     expand = False,
#     verbose = True,
#     overwrite = False
# )
