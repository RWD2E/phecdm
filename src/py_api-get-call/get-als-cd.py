import os
import api_get_bioportal as apibp
import api_get_rxnav as apirxnav

path_to_tgt = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'res','valueset_autogen')

# diagnostics 
# apibp.batch_write_vs_json(
#      path_to_search_catalog = path_to_tgt,
#      search_catalog_name = 'als-dx_input'
#     )

# real world endpoints
# apibp.batch_write_vs_json(
#      path_to_search_catalog = path_to_tgt,
#      search_catalog_name = 'als-tx_input'
#     )

# medications    
rxnav_cls = apirxnav.RxNavSearch()
# print(rxnav_cls.get_ndc_from_rxcui('349332'))
# print(rxnav_cls.get_rxcui_all('349332'))
# print(rxnav_cls.get_rxcui_from_atc('N06A'))
# print(rxnav_cls.get_rxcui_from_str('Lexapro 10 mg oral tablet'))
apirxnav.batch_write_rx_code_json(
    path_to_save = path_to_tgt, #absolute path,
    filename_to_save = 'als-rx',
    sterms = ['riluz','endarovone'],
    sterm_type = 'string',
    verbose=True
)