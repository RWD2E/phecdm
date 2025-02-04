import pandas as pd
import json
import urllib.request as urlreq
import os
import re

def split_part_multisql(
    which_sql, #["snow","postgres","spark","mysql","sqlserver","oracle"]
    string,
    delimiter,
    index
):
    sqlqry = ''
    if which_sql in ('snow','postgres'):
        sqlqry += '''
            split_part('''+ string +''','''+ "'"+ delimiter +"'"+''','''+ str(index) +''')
        '''
    elif which_sql in ('spark','mysql'):
        sqlqry += '''
            substring_index('''+ string +''','''+ "'"+ delimiter +"'"+''','''+ str(index) +''')
        '''
    elif which_sql == 'sqlserver':
        sqlqry += '''
            string_split('''+ string +''','''+ "'"+ delimiter +"'" +''','''+ str(index) +''')
        '''
    elif which_sql == 'sqlserver':
        sqlqry += '''
            regexp_substr('''+ string +''', [^'''+ "'"+ delimiter +"'" +''']+,1,'''+ str(index) +''')
        '''
    else:
        Warning("The SQL version is not supported!")

    return sqlqry

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


def json2ref(
    json_url, #url to valueset json file (rawcontent)
    save_csv_to #location to save the csv file
):
    # load json file
    json_url = urlreq.urlopen(json_url)
    json_file = json.loads(json_url.read())
    
    # collect selected keys
    csv_lst = []
    for item in json_file:
        for chunk in item["compose"]["include"]:
            csv_lst.append({
                'id':item["id"],
                'name':item["name"],
                'description':item["description"],
                'codesystem':chunk["system"],
                'code':sum([x["value"] for x in chunk["filter"]], [])
        })
        
    # create DF from json data and expand
    df = pd.DataFrame(csv_lst)
    expanded_df = df.explode('code')

    # save to csv
    expanded_df.to_csv(save_csv_to,index=False)
    return('new valueset saved as ref csv')

class QueryFromJson:
    def __init__(
        self,
        url, #url to json file
        sqlty, #which type of sql ["snow","postgres","spark","mysql","sqlserver","oracle"]
        cd_field, #code field
        cdtype_field, #code type field
        other_fields, #list of other fields needed to be retained
        srctbl_name, #source table name
        sel_keys = list() #list of selected keys to be queried, can be empty
    ):
        self.url = url
        self.sqlty = sqlty
        self.cd_field= cd_field
        self.cdtype_field = cdtype_field
        self.other_fields = other_fields
        self.srctbl_name = srctbl_name
        self.sel_keys = sel_keys

    @staticmethod
    def gen_cdtype_encoder():
        cdtype_encoder = {
            "icd9cm":input("Enter Code Type Value for icd9cm: "),
            "icd10cm":input("Enter Code Type Value for icd10cm: "),
            "icd9proc": input("Enter Code Type Value for icd9proc: "),
            "icd10pcs": input("Enter Code Type Value for icd10pcs: "),
            "cpt": input("Enter Code Type Value for cpt: "),
            "hpc": input("Enter Code Type Value for hpc: "),
            "drg": input("Enter Code Type Value for drg: "),
            "loinc": input("Enter Code Type Value for loinc: ")
        }
        return(cdtype_encoder)
    
    @staticmethod
    def parse_filter(lst):
        cddict = {}
        for item in lst:
            if item["property"]=="codePrecision" and item["op"]=="descendent-of":
                decimal = [len(x.split('.')[1]) if '.' in x else 0 for x in item["value"]]
                try: cddict["0"] = [item["value"][index] for index, current_value in enumerate(decimal) if current_value == 0]
                except ValueError: return None
                try: cddict["1"] = [item["value"][index] for index, current_value in enumerate(decimal) if current_value == 1]
                except ValueError: return None
                try: cddict["2"] = [item["value"][index] for index, current_value in enumerate(decimal) if current_value == 2]
                except ValueError: return None
                try: cddict["3"] = [item["value"][index] for index, current_value in enumerate(decimal) if current_value == 3]
                except ValueError: return None
                try: cddict["04"] = [item["value"][index] for index, current_value in enumerate(decimal) for val in item["value"] if current_value == 0 and len(val) >= 4]
                except ValueError: return None

            elif item["property"]=="codeRange" and item["op"]=="in":
                cddict["9"] = []
                for x in item["value"]:
                    key_quote = [str(y) for y in list(range(int(x.split('-')[0]),int(x.split('-')[1])+1))]
                    cddict["9"].extend(key_quote)

            elif item["property"]=="codeList" and item["op"]=="in":
                cddict["9"] = item["value"]

            else:
                print("filter propery or op not defined in the valuset json file.")
                pass
        
        cddict = {k: v for k, v in cddict.items() if v}
        return(cddict)

    @staticmethod
    def add_quote(lst):
        lst_quote = ["'"+str(x)+"'" for x in lst]
        return (lst_quote)
        
    def gen_qry_ref(self):     
        # load json valueset file
        json_url = urlreq.urlopen(self.url)
        json_file = json.loads(json_url.read())

        # load cdtype mapping
        cdtype_map = self.gen_cdtype_encoder()

        # generate reference dictionary for where clause
        qry_out = {}
        for x in json_file:  
            qryx_orlst = []
            for y in x["compose"]["include"]:
                # code type 
                qry = self.cdtype_field + "='" + cdtype_map[y["system"]] + "'"

                # codes
                qryxy_orlst = []
                cdref = self.parse_filter(y["filter"])
                if '0' in cdref:
                    qryxy_orlst.append(
                        split_part_multisql(self.sqlty,self.cd_field,'.',1) + ''' in ('''+ ','.join(self.add_quote(cdref["0"])) +''')
                    ''')
                elif '1' in cdref:
                    qryxy_orlst.append('''
                        substring('''+ self.cd_field +''',1,5) in ('''+ ','.join(self.add_quote(cdref["1"])) +''')
                    ''')
                elif '2' in cdref:
                    qryxy_orlst.append('''
                        substring('''+ self.cd_field +''',1,6) in ('''+ ','.join(self.add_quote(cdref["2"])) +''')
                    ''')
                elif '04' in cdref:
                    qryxy_orlst.append('''
                        substring('''+ self.cd_field +''',1,4) in ('''+ ','.join(self.add_quote(cdref["04"])) +''')
                    ''')
                else:
                    cdref39 = (cdref.get("3") or []) + (cdref.get("9") or [])
                    qryxy_orlst.append('''
                        ''' + self.cd_field + ''' in ('''+ ','.join(self.add_quote(cdref39)) +''')
                    ''')
                
                qryx_orlst.append(qry + ''' and (''' + ' or '.join(qryxy_orlst) + ''')''')

            # add query entry to dict
            qry_out[x["name"]] = ') OR ('.join(qryx_orlst)

        return qry_out 
    
    def gen_qry(self):
        selqry_lst = []
        qry_dict = self.gen_qry_ref()
        for k,v in qry_dict.items():
            if len(self.sel_keys) == 0 or k in self.sel_keys:
                all_fields = self.other_fields + [self.cd_field,self.cdtype_field]
                selqry_lst.append('''
                    select ''' + ','.join(all_fields) + 
                        " ,'"+ k +"' as CD_GRP" '''
                    from '''+ self.srctbl_name +'''
                    where ('''+ v +''')
                ''')
        complt_qry = ' union all '.join(selqry_lst)
        return(complt_qry)

