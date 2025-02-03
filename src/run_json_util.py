# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-als-cde.json"
# )
# als_vs = JsonBlockVS(filepath = fp,idstarter='C')
# print(als_vs.get_existing_id())
# print(als_vs.generate_new_id())
# print(als_vs.create_json_data_block())
# print(als_vs.add_json_block())


# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-mmm-cde.json"
# )
# mmm_vs = JsonBlockVS(filepath = fp,idstarter='M')
# print(mmm_vs.add_json_block())

# fp = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'res','valueset_curated',"vs-t2dm-cde.json"
# )
# t2dm_vs = JsonBlockVS(filepath = fp,idstarter='DM')
# print(t2dm_vs.get_existing_id())
# print(t2dm_vs.generate_new_id())
# print(t2dm_vs.add_json_block())

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


# json2ref(
#     json_url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-comorb-OBCMI.json',
#     save_csv_to = 'C:/repos/phecdm/ref/OBCMI_ICD.csv'
# )

# vs_obcmi = QueryFromJson(
#     url = 'https://raw.githubusercontent.com/RWD2E/phecdm/refs/heads/main/res/valueset_curated/vs-comorb-OBCMI.json',
#     cd_field = 'DX',
#     cdtype_field = 'DX_TYPE'
# )
# vs_obcmi.gen_cdtype_encoder()
# print(vs_obcmi.gen_qry())