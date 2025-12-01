import os
import sys
from gen_vs_json_utils import QueryFromJson, JsonBlockVS, json2ref, split_part_multisql, expand_range


# vs_als = QueryFromJson(
#     url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-als-cde.json',
#     sqlty = 'spark',
#     cd_field = 'CONCEPT_CODE',
#     cdtype_field = 'VOCABULARY_ID',
#     srctbl_name = "CONCEPT",
#     other_fields=["concept_id","concept_name","domain_id"]
# )
# print(vs_als.gen_qry())

# vs_smm = QueryFromJson(
#     url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-mmm-cde.json',
#     sqlty = 'spark',
#     cd_field = 'CONCEPT_CODE',
#     cdtype_field = 'VOCABULARY_ID',
#     srctbl_name = "CONCEPT",
#     other_fields=["concept_id","concept_name","domain_id"],
#     sel_keys = ['bpt','hys']
# )
# print(vs_smm.gen_qry_ref())
# print(vs_smm.gen_qry())

# vs_delivery = QueryFromJson(
#     url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-mmm-cde.json',
#     sqlty = 'spark',
#     cd_field = 'CONCEPT_CODE',
#     cdtype_field = 'VOCABULARY_ID',
#     srctbl_name = "CONCEPT",
#     other_fields=["concept_id","concept_name","domain_id"],
#     sel_keys = ['vaginalDelivery','cSection']
# )
# print(vs_delivery.gen_qry_ref())
# print(vs_delivery.gen_qry())


fp = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'res','valueset_curated',"vs-cde-als.json"
)
als_vs = JsonBlockVS(filepath = fp,idstarter='C',idlength = 6)
# print(als_vs.get_existing_id())
# print(als_vs.generate_new_id())
# print(als_vs.create_json_data_block())
print(als_vs.add_json_block())


# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-mmm-cde.json"
# )
# mmm_vs = JsonBlockVS(filepath = fp,idstarter='M',idlength=6)
# print(mmm_vs.add_json_block())

# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-cde-dm.json"
# )
# t2dm_vs = JsonBlockVS(filepath = fp,idstarter='DM',idlength=5)
# print(t2dm_vs.get_existing_id())
# print(t2dm_vs.generate_new_id())
# t2dm_vs.add_json_block()

# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-comorb-OBCMI.json"
# )
# comorb_vs = JsonBlockVS(filepath = fp,idstarter='M',idlength=7)
# print(comorb_vs.generate_new_id())
# print(comorb_vs.add_json_block())

# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-t2dm-cde.json"
# )
# comorb_vs = JsonBlockVS(filepath = fp,idstarter='SDM',idlength=8)
# print(comorb_vs.add_json_block())

# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-cde-kd.json"
# )
# kd_vs = JsonBlockVS(filepath = fp,idstarter='KD',idlength=5)
# print(kd_vs.get_existing_id())
# print(kd_vs.generate_new_id())
# kd_vs.add_json_block()



# json2ref(
#     json_url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-comorb-OBCMI.json',
#     save_csv_to = 'C:/repos/phecdm/ref/OBCMI_ICD.csv'
# )


# json2ref(
#     json_url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-als-cde.json',
#     save_csv_to = 'C:/repos/phecdm/ref/als_cde.csv'
# )