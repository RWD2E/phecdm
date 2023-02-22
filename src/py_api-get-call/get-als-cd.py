import os
import api_get_bioportal as apibp
import api_get_rxnav as apirxnav

path_to_search_input = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'res','valueset_autogen')

# diagnostics 
# apibp.batch_write_vs_json(
#      path_to_search_input
#     ,'als-dx_input'
#     )

# real world endpoints
apibp.batch_write_vs_json(
     path_to_search_input
    ,'als-tx_input'
    )

# medications
# sterms = ['riluzole']
# apirxnav.batch_write_ndc_json(path_to_search_input,
#                               'als-rx_output',sterms)
     
