import os
import api_get_vsac as apivsac
import api_get_rxnav as apirxnav

path_to_tgt = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'res','valueset_autogen')

# validation
vsac_cls = apivsac.VsacSearch()
# print(vsac_cls.get_cd_from_oid_svs("2.16.840.1.113883.3.464.1003.196.12.1481"))
# print(vsac_cls.get_cd_from_oid_svs("2.16.840.1.113883.3.464.1003.1049"))


# manual list of oids
# ref: https://ecqi.healthit.gov/measure-data-elements/173701
oid_lst = [
    "2.16.840.1.113883.3.464.1003.196.12.1480",
    "2.16.840.1.113883.3.464.1003.196.12.1481",
    "2.16.840.1.113883.3.464.1003.196.12.1522",
    "2.16.840.1.113883.3.464.1003.196.12.1523",
    "2.16.840.1.113883.3.464.1003.1043",        
    "2.16.840.1.113883.3.464.1003.1044",
    "2.16.840.1.113883.3.464.1003.1049",
    "2.16.840.1.113883.3.464.1003.1050",
    "2.16.840.1.113883.3.464.1003.1051",
    "2.16.840.1.113883.3.464.1003.1052",
    "2.16.840.1.113883.3.464.1003.1053",
    "2.16.840.1.113883.3.464.1003.1054",
    "2.16.840.1.113883.3.464.1003.1055",
    "2.16.840.1.113883.3.464.1003.1056",
    "2.16.840.1.113883.3.464.1003.1057",
    "2.16.840.1.113883.3.464.1003.1058",
    "2.16.840.1.113883.3.464.1003.1059",
    "2.16.840.1.113883.3.464.1003.1060",
    "2.16.840.1.113883.3.464.1003.1062",
    "2.16.840.1.113883.3.464.1003.1063",
    "2.16.840.1.113883.3.464.1003.1065",
    "2.16.840.1.113883.3.464.1003.1067"
]

apivsac.batch_write_rx_code_json(
    path_to_save = path_to_tgt, #absolute path,
    filename_to_save = 'pim-rx',
    sterms = oid_lst,
    verbose=True
)