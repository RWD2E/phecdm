import pandas as pd
import json
import urllib.request as urlreq
import os
import re

class JsonBlockVS:
    TOPIC_ENCODER = {
        "1": "participant characteristics",
        "2": "participant history and family history",
        "3": "diease/injury related events",
        "4": "assessment and examinations",
        "5": "treatment/intervention",
        "6": "outcomes and endpoints"
    }

    PURPOSE_ENCODER = {
        "1": {
            "1":"demographics",
            "2":"social status"
        },
        "2":{
            "1":"family history",
            "2":"medical history"
        },
        "3": {
            "1":"symptom/sign and diagnosis criteria",
            "2":"genetics",
            "3":"comorbidities"
        },
        "4":{
            "1":"laboratory tests and biospecimens/biomarkers",
            "2":"imaging diagnostics",
            "3":"non-imaging diagnostics",
            "4":"physical/neurological examination",
            "5":"vital signs and other body measures"
        },
        "5":{
            "1":"drugs",
            "2":"devices",
            "3":"precedures"
        },
        "6":{
            "1":"muscle strength testing",
            "2":"cognitive",
            "3":"functional outcomes",
            "4":"pulmonary function testing/respiratory status",
            "5":"subjective assessments/patient and caregiver reported outcomes",
            "6":"upper motor neuron signs/neuromuscular excitability",
            "7":"severe maternal morbidity"
        }
    }

    CLASS_ENCODER = {
        "1": "core",
        "2": "recommended",
        "3": "supplemental",
        "4": "exploratory"
    }

    VALUETYPE_ENCODER = {
        "1": "nominal",
        "2": "ordinal",
        "3": "discrete",
        "4": "continuous",
        "5": "boolean"
    }

    VALUERANGE_ENCODER = {
        "1": {}, 
        "2": {},
        "3": {
            "min":int(),
            "max":int()
        },
        "4": {
            "min":float(),
            "max":float()
        },
        "5": {
            "0": "absence",
            "1": "presence"
        }
    }

    SYSTEM_ENCODER = {
        "1":"loinc",
        "2":"icd9cm",
        "3":"icd9proc",
        "4":"icd10cm",
        "5":"icd10pcs",
        "6":"snomedct",
        "7":"cpt4",
        "8":"hpc",
        "9":"ndc",
        "10":"atc",
        "11":"rxnorm",
        "12":"ndfrt",
        "13":"cvx",
        "14":"drg",
        "15":"npiTaxonomy",
        "16":"cmsSpecialty",
        "99":"other"
    }

    PROPERTY_ENCODER = {
        "1":"codePrecision",
        "2":"codeRange",
        "3":"codeList"
    }

    OP_ENCODER = {
        "1":"=",
        "2":"is-a",
        "3":"descendent-of",
        "4":"is-not-a",
        "5":"regex",
        "6":"in",
        "7":"not-in",
        "8":"generalizes",
        "9":"child-of",
        "10":"descendent-leaf",
        "11":"exists"
    }
    

    def __init__(self,filepath,idstarter,idlength):
        self.filepath = filepath
        self.idstarter = idstarter
        self.idlength = idlength
    
    def get_existing_id(self):
        with open(self.filepath,'r') as file:
            jdata = json.load(file)
        existing_id_num = [int(num) for item in jdata for num in re.findall(r'\d+', item['id'])]
        return existing_id_num

    def generate_new_id(self) -> str:
        new_id = max(self.get_existing_id())+1
        return self.idstarter + str(new_id).zfill(self.idlength)

    # Function to create a JSON data block
    def create_json_data_block(self):
        data_block = {
            "id": self.generate_new_id(),
            "name": input("Enter name: "),
            "description": input("Enter description: ")
        }
        # prompt topic selection
        for key, value in self.TOPIC_ENCODER.items(): print(f"{key}:{value}")
        topic_choice = input("Enter choice: ")
        data_block["topic"] = self.TOPIC_ENCODER[topic_choice]

        # prompt purpose selection
        for key, value in self.PURPOSE_ENCODER[topic_choice].items(): print(f"{key}:{value}")
        data_block["purpose"] = self.PURPOSE_ENCODER[topic_choice][input("Enter choice: ")]

        # prompt relatedArtifact selections
        data_block["relatedArtifact"] = dict()
        for key, value in self.CLASS_ENCODER.items(): print(f"{key}:{value}")
        data_block["relatedArtifact"]["class"] = self.CLASS_ENCODER[input("Enter choice: ")]

        for key, value in self.VALUETYPE_ENCODER.items(): print(f"{key}:{value}")
        valuetype_choice = input("Enter choice: ")
        data_block["relatedArtifact"]["valueType"] = self.VALUETYPE_ENCODER[valuetype_choice]
        data_block["relatedArtifact"]["valueRange"] = self.VALUERANGE_ENCODER[valuetype_choice]

        # prompt coding system selection
        # allow multiple include blocks
        data_block["compose"] = {
            "include": []
        }
        while True:
            add_include = input("Do you want to add an 'include' block? (1=yes/0=no): ").strip().lower()
            if add_include == '1':
                for key, value in self.SYSTEM_ENCODER.items(): print(f"{key}:{value}")
                include_entry = {
                    "system": self.SYSTEM_ENCODER[input("Enter choice: ")],
                    "concept": [],
                    "filter": []
                }
                data_block["compose"]["include"].append(include_entry)
                
                # optional concept block
                while True:
                    add_concept = input("Do you want to add a concept? (1=yes/0=no): ").strip().lower()
                    if add_concept == '1':
                        concept_entry = {
                            "code": input("Enter code: "),
                            "display": input("Enter display: ")
                        }
                        data_block["compose"]["include"][-1]["concept"].append(concept_entry)
                    else:
                        if not data_block["compose"]["include"][-1]["concept"]:
                            del data_block["compose"]["include"][-1]["concept"]  # Remove if empty
                        break
                    
                # optional filter block
                while True:
                    add_filter = input("Do you want to add a filter? (1=yes/0=no): ").strip().lower()
                    if add_filter == '1':
                        for key, value in self.PROPERTY_ENCODER.items(): print(f"{key}:{value}")
                        property_choice = input("Enter property: ")
                        for key, value in self.OP_ENCODER.items(): print(f"{key}:{value}")
                        op_choice = input("Enter operation: ")
                        input_value = input("Enter value (separated by comma): ")
                        filter_entry = {
                            "property": self.PROPERTY_ENCODER[property_choice],
                            "op": self.OP_ENCODER[op_choice],
                            "value": [item.strip() for item in input_value.split(',')]
                        }
                        data_block["compose"]["include"][-1]["filter"].append(filter_entry)
                    else:
                        if not data_block["compose"]["include"][-1]["filter"]:
                            del data_block["compose"]["include"][-1]["filter"]  # Remove if empty
                        break
            else:
                break

        return data_block

    def add_json_block(self):
        new_block = self.create_json_data_block()
        print(new_block)
        confirm_add = input("Do you want to add the new json block? (1=yes/0=no): ").strip().lower()
        if confirm_add == '1':
            # open existing file and add json block
            with open(self.filepath,'r') as file:
                jdata = json.load(file)
            jdata.append(new_block)
            # overwrite with the new json file
            with open(self.filepath,'w') as file:
                json.dump(jdata,file,indent = 4)
            return "The new json data block is added"
        else:
            return "The new json data block is rejected"

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

def json2ref(
    json_url, #url to valueset json file
    csv_file #location to save the csv file
):
    # load json file
    json_url = urlreq.urlopen(json_url)
    json_file = json.loads(json_url.read())

    # collect selected keys
    csv_lst = []
    for item in json_file:
        csv_lst.append({
            "id":item["id"],
            "name":item["name"],
            "description":item["description"],
            "codesystem":[x["system"] for x in item["compose"]["include"]],
            "code":[x["value"] for x in item["compose"]["include"]]
        })

    # create DF from json data
    df = pd.DataFrame(csv_lst)

    # save
    return(csv_lst)

json2ref

# def json2qry(
#     url #url to json file
# ):
#     json_url = urlreq.urlopen(url)
#     json_file = json.loads(json_url.read())
#     qry_lst = []
#     def add_quote(lst):
#         lst_quote = ["'"+str(x)+"'" for x in lst]
#         return (lst_quote)
#     for k,v in json_file.items():
#         for cd,sig in v.items():
#             if cd=='long': continue
#             # entail the range
#             if 'range' in sig:
#                 for x in sig['range']:
#                     key_quote = [str(y) for y in list(range(int(x.split('-')[0]),int(x.split('-')[1])+1))]
#                     sig['exact'].extend(key_quote)

#             # generate dynamic queries
#             qry = '''
#                 select ''' + "'" + k + "'" + ''' as CD_GRP, 
#                        ''' + "'" + v['long'] + "'" + ''' as CD_GRP_LONG,
#                        concept_id,concept_name,concept_code,vocabulary_id,domain_id
#                 from concept
#                 where vocabulary_id = '''+ "'" + cd.upper() + "'" +''' and
#             '''
#             if 'icd' in cd and 'pcs' not in cd:
#                 where_lev0 = '''substring_index(concept_code,'.',1) in ('''+ ','.join(add_quote(sig['0'])) +''')''' if sig['lev0'] else None
#                 where_lev1 = '''substring(concept_code,1,5) in ('''+ ','.join(add_quote(sig['1'])) +''')''' if sig['lev1'] else None
#                 where_lev2 = '''substring(concept_code,1,6) in ('''+ ','.join(add_quote(sig['2'])) +''')''' if sig['lev2'] else None
#                 where_nonempty = [s for s in [where_lev0,where_lev1,where_lev2] if s is not None]

#                 qry += '''
#                 (
#                      ''' + ' or '.join(where_nonempty) + '''  
#                 )         
#                 '''
#             else:
#                 qry += '''
#                 (
#                      concept_code in ('''+ ','.join(add_quote(sig['exact'])) +''')
#                 )         
#                 '''
#             qry_lst.append(qry)
            
#     return qry_lst





