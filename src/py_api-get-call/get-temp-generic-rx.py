import os
import api_get_rxnav as apirxnav
import pandas as pd

path_to_tgt = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
            )
        ),
    'res','valueset_autogen'
)

rxnav_cls = apirxnav.RxNavSearch()

# fenofibrate
# gn_lst = rxnav_cls.get_rxcui_from_str('fenofibrate')
# gn_df = pd.DataFrame(gn_lst)
# gn_df.to_csv('C:/repos/phecdm/ref/fenofibrate_rxcui.csv',index = False,quoting=1)

# debug
# gn_lst = rxnav_cls.get_rxcui_from_str('#22 syringe 1 1/2" needle')
# gn_lst = rxnav_cls.get_rxcui_from_str('22 syringe 1 1/2" needle')
gn_lst = rxnav_cls.get_rxcui_from_str('Tegaderm Film 4"x4-3/4"')
print(gn_lst)
