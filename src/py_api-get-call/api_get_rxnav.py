import json
import requests
import api_call_utils as apiutil
import re
import time

class RxNavSearch:
    '''
    search RxNav API and return requested results in human-readable format
    https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html
    '''
    # global values
    API_URI = apiutil.get_access_info()['umls-api']['rxnav-endpoint']

    # instance values
    def __init__(self):
        # rxnav API doesn't require access token
        pass
    
    # get list of ndc codes for given rxcui code
    def get_ndc_from_rxcui(self,rxcui='000') -> list:
        '''
        rxnav API call to collect NDC list for a given RXCUI code
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getNDCs.html
        '''
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/rxcui/{rxcui}/ndcs.json')
        items  = json.loads(response.text)
        if not items["ndcGroup"]["ndcList"]:
            return ([])
        else:
            return(items["ndcGroup"]["ndcList"]["ndc"]) 

    def get_rxcui_all(
            self,
            rxcui,
            tty_lst=['SCD','SCDC','SCDF','SCDG','SBD','SBDC','SBDF','SBDG','IN','MIN','PIN']
        ):
        '''
        rxnav API call to collect all listed levels of RXCUI
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getAllRelatedInfo.html
        '''
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/rxcui/{rxcui}/allrelated.json')
        results = json.loads(response.text)
        all_medications = []
        for group in results['allRelatedGroup']['conceptGroup']:
            if 'conceptProperties' in group and group['tty'] in tty_lst:
                for item in group['conceptProperties']:
                    rxcui_add = item
                    rxcui_add.pop('umlscui')
                    rxcui_add.pop('language')
                    rxcui_add.pop('synonym')
                    rxcui_add['ndc'] = self.get_ndc_from_rxcui(item['rxcui'])
                    all_medications.append(rxcui_add)
        return (all_medications)
    
    def get_rxcui_from_str(self,term:str,maxEntries=20,keep_rk=1):
        '''
        rxnav API call to find approximate match
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getApproximateMatch.html
        '''
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/approximateTerm.json?term={term}&maxEntries={maxEntries}&option=0')
        results = json.loads(response.text)
        rxcui_candidates = []
        rxcui_lst = []
        try:
            for candidate in results['approximateGroup']['candidate']:
                if int(candidate['rank']) <= keep_rk and candidate['rxcui'] not in rxcui_candidates:
                    # when term only contains ingredient string, the results are often rxcui at ingredient level
                    rxcui_candidates.append(candidate['rxcui'])

            # Loop through rxcui_candidates 
            for ing in rxcui_candidates:
                allrelacodes = self.get_rxcui_all(ing)
                rxcui_lst.extend(allrelacodes)   
        except:
            print(f"No RXCUI found for ingredient '{term}'.")
        
        # output results
        return(rxcui_lst)
         
    def get_rxcui_from_atc(self,class_code):
        '''
        rxnav API call to find all relevant rxcui codes under a ATC class
        '''
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/rxclass/classMembers.json?classId={class_code}&relaSource=ATC')
        results = json.loads(response.text)
        ingredients = [r['minConcept'] for r in results['drugMemberGroup']['drugMember']]

        # Loop through ingredients
        rxcui_lst = []
        for ing in ingredients:
            allrelacodes = self.get_rxcui_all(ing['rxcui'])
            ing['allrelacodes'] = allrelacodes
            rxcui_lst.append(ing)

        # output results
        return(rxcui_lst)   
    
    def get_cls_from_rxcui(self,rxcui):
        '''
        rxnav API call to map a rxcui code to a ATC or VA or MEDRT (may_treat) class
        '''
        # time.sleep(0.05)
        cls_lst=[]
        cls_set=set()
        for clsty in ['ATC','VA','MEDRT']:
            call_url = f'{self.API_URI}/rxclass/class/byRxcui.json?rxcui={rxcui}&relaSource={clsty}'
            if clsty == 'MEDRT':
                call_url += '&relas=may_treat'
            response = requests.get(call_url)
            results = json.loads(response.text)
            try: 
                for r in results['rxclassDrugInfoList']['rxclassDrugInfo']:
                    cls_dict = r['rxclassMinConceptItem']
                    # dedup
                    hash_dict = frozenset(cls_dict.items())
                    if hash_dict not in cls_set:
                        cls_set.add(hash_dict)
                        cls_lst.append(cls_dict)
            except:
                print(f"No {clsty} class found for {rxcui}'.")
        # output results
        return(cls_lst) 

    def get_rxcui_from_va(self,class_code):
        '''
        rxnav API call to find all relevant rxcui codes under a VA-NDFRT/MEDRT class
        https://lhncbc.nlm.nih.gov/RxNav/assets/publications/MED-RT_Documentation.pdf
        '''
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/rxclass/classMembers.json?classId={class_code}&relaSource=VA&rela=has_VAClass')
        results = json.loads(response.text)
        ingredients = [r['minConcept'] for r in results['drugMemberGroup']['drugMember']]

        # Loop through ingredients
        rxcui_lst = []
        for ing in ingredients:
            allrelacodes = self.get_rxcui_all(ing['rxcui'])
            ing['allrelacodes'] = allrelacodes
            rxcui_lst.append(ing)

        # output results
        return(rxcui_lst)  
    
    def get_rxcui_details(self,rxcui,expand=False) -> dict:
        '''
        rxnav API call to collect all standardized properties and related attributes
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getAllProperties.html
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getAllRelatedInfo.html
        '''
        # time.sleep(0.05)
        # extract strength and unit info
        response = requests.get(f'{self.API_URI}/rxcui/{rxcui}/allProperties.json?prop=ALL')
        results = json.loads(response.text)
        std_drug_str = {"rxcui":rxcui}
        for prop in results['propConceptGroup']['propConcept']:
            # collect normalized rx name
            if prop['propName'] == 'RxNorm Name':
                std_drug_str['name'] = [re.sub(r'\[[^]]*\]','',x.lower()) for x in prop['propValue'].split(" / ")] #->list
            # parse strength info
            elif prop['propName'] == 'AVAILABLE_STRENGTH':
                std_drug_str['str-unit'] = prop['propValue'].lower().split(" / ") #->list
                std_drug_str['str'] = [x.split(' ')[0] for x in std_drug_str['str-unit']]
                std_drug_str['unit'] = [x.split(' ')[1] for x in std_drug_str['str-unit']]
            
        # extract ingredient info
        response = requests.get(f'{self.API_URI}/rxcui/{rxcui}/allrelated.json')
        results = json.loads(response.text)
        for prop in results['allRelatedGroup']['conceptGroup']:
            # get dose form
            if prop['tty'] == 'DF' and 'conceptProperties' in prop:
                std_drug_str['dose-form'] = [x["name"].lower() for x in prop['conceptProperties']]

            # get ingredient and ingredient codes
            if prop['tty'] == 'IN' and 'conceptProperties' in prop:
                std_drug_str['in'] = [x["name"].lower() for x in prop['conceptProperties']]
                std_drug_str['in-code'] = [x["rxcui"].lower() for x in prop['conceptProperties']]

        # expand output
        if expand:
            # {rxcui:, component:[]}
            expand_n = len(std_drug_str['name'])
            std_drug_str_un = [
                {key: std_drug_str[key][i] for key in ['name','str-unit','str','unit','in']}
                 for i in range(expand_n)
            ]
            std_drug_str = {
                'rxcui': rxcui,
                'dose-form':std_drug_str["dose-form"][0],
                'component': std_drug_str_un
            } 
        
        # output results
        return (std_drug_str)
    
    def get_rxcui_history(self,rxcui,expand=False)->dict:
        '''
        rxnav NPI call to collect information for a historial RXCUI
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getRxcuiHistoryStatus.html
        '''
        # time.sleep(0.05)
        # extract strength and unit info
        response = requests.get(f'{self.API_URI}/rxcui/{rxcui}/historystatus.json')
        results = json.loads(response.text)
        std_drug_str = {"rxcui":rxcui}

        for prop, val in results['rxcuiStatusHistory'].items():
            # get code status
            if prop == 'metaData':
                std_drug_str['status'] = val['status']
                std_drug_str['activeStartDate'] = val['activeStartDate']
                std_drug_str['activeEndDate'] = val['activeEndDate']
            # get rxnorm name
            if prop == 'attributes':
                std_drug_str['name'] = val['name']
                std_drug_str['tty'] = val['tty']
            # get ingredient info
            if prop == 'definitionalFeatures':
                in_lst = val['ingredientAndStrength']
                std_drug_str['in'] = [x['baseName'] for x in in_lst]
                std_drug_str['in-code'] = [x['baseRxcui'] for x in in_lst]
                std_drug_str['str'] = [x['numeratorValue'] for x in in_lst]
                std_drug_str['unit'] = [x['numeratorUnit'] for x in in_lst]
                try:   
                    std_drug_str['in-code-active'] = [x['activeIngredientRxcui'] for x in in_lst]                
                except:
                    print('No active ingredients.')

                # get potential active scd codes
                if 'scdConcept' in val.keys():
                    std_drug_str['scd-code'] = val['scdConcept']['scdConceptRxcui']
                    std_drug_str['scd-name'] = val['scdConcept']['scdConceptName']
            
        # expand output
        if expand:
            # {rxcui:, component:[]}
            comp_lst = ['in','in-code','str','unit','in-code-active']
            expand_n = len(std_drug_str['in'])
            std_drug_str_un = [
                {key: std_drug_str[key][i] for key in comp_lst}
                for i in range(expand_n)
            ]
            std_drug_str = {key: value for key, value in std_drug_str.items() if key not in comp_lst}
            std_drug_str['component'] = std_drug_str_un

        # output results
        return (std_drug_str)


    def get_ndc_details(self,ndc_code,expand=False):
        '''
        rxnav API call to find all mappable properties about a single NDC code
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getNDCProperties.html
        '''   
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/ndcproperties.json?id={ndc_code}&ndcstatus=ALL')
        results = json.loads(response.text)

        # loop through ndc property list
        ndc_ppty = {}
        for ppty in results['ndcPropertyList']['ndcProperty']:
            try:
                # sub-API call to collect ingredient, strength, dosage form
                ndc_ppty['ndc'] = ndc_code
                ndc_ppty['rxcui'] = ppty['rxcui'] 
                ndc_ppty.update(self.get_rxcui_details(ppty['rxcui'],expand))
            except:
                print(f"NDC can't be mapped to RXCUI or RXCUI is inactive.")
                
            # not all NDC has packaging info
            try: 
                ndc_ppty['packaging'] = ppty['packagingList']['packaging'].lower()               
            except:
                ndc_ppty['packaging'] = '' 
        
        # output results
        return(ndc_ppty) 

def batch_write_ndc_details_json(
    path_to_save, #absolute path,
    filename_to_save,
    sterms:list,
    expand=False,
    verbose=True,
    overwrite=True
) -> list:
    '''
    generate a list of dist of standardized properties for 
    NDC code list
    '''
    ppty_lst = []
    rxnav_cls = RxNavSearch()
    for term in sterms:
        time.sleep(0.05)
        try:
            ndc_ppty = rxnav_cls.get_ndc_details(term,expand)
            ppty_lst.append(ndc_ppty)
        except:
            print(f"NDC:{term} not found.")

        # report progress
        if verbose:
            print(f'finish mapping for NDC:{term}.')

    json_file_path = f"{path_to_save}/{filename_to_save}.json"
    if not overwrite:
        try:
            # Read existing JSON data from the file
            with open(json_file_path, 'r') as file:
                existing_data = json.load(file)
            # Append new data to the existing data
            existing_data.extend(ppty_lst)
            # Update existing file
            ppty_lst = existing_data
        except FileNotFoundError:
            print(f"The file '{json_file_path}' was not found.")
    
    # write single dictionary to json
    with open(json_file_path,"w",encoding='utf-8') as writer: 
        json.dump(ppty_lst, writer, ensure_ascii=False, indent=4)

def batch_write_rxcui_details_json(
    path_to_save, #absolute path,
    filename_to_save,
    sterms:list,
    expand=False,
    verbose=True,
    overwrite=True
) -> list:
    '''
    generate a list of dist of standardized properties for 
    RXCUI code list
    '''
    ppty_lst = []
    rxnav_cls = RxNavSearch()
    for term in sterms:
        # time.sleep(0.05)
        try:
            rxcui_ppty = rxnav_cls.get_rxcui_history(term,expand)
            try:
                rxcui_ppty['classes'] = rxnav_cls.get_cls_from_rxcui(term)
            except:
                print(f"No class found for {term}.")
            ppty_lst.append(rxcui_ppty)
        except:
            print(f"RXCUI:{term} not found.")

        # report progress
        if verbose:
            print(f'finish mapping for RXCUI:{term}.')
    
    json_file_path = f"{path_to_save}/{filename_to_save}.json"
    if not overwrite:
        try:
            # Read existing JSON data from the file
            with open(json_file_path, 'r') as file:
                existing_data = json.load(file)
            # Append new data to the existing data
            existing_data.extend(ppty_lst)
            # Update existing file
            ppty_lst = existing_data
        except FileNotFoundError:
            print(f"The file '{json_file_path}' was not found.")
    
    # write single dictionary to json
    with open(json_file_path,"w",encoding='utf-8') as writer: 
        json.dump(ppty_lst, writer, ensure_ascii=False, indent=4)

def batch_write_rx_code_json(
    path_to_save, #absolute path,
    filename_to_save,
    sterms:list,
    sterm_type:str,
    verbose=True
):
    '''
    identify rxcui codes for each term in sterms, then
    search rxnav database to identify all cooresponding ndc codes
    '''
    dict_agg = {}
    for term in sterms:
        rxnav_cls = RxNavSearch()
        # search rxcui by rxcui
        if sterm_type == "rxcui":
            code_lst = rxnav_cls.get_ndc_from_rxcui(term)
        # search rxcui by atc class code
        elif sterm_type == "atc":
            code_lst = rxnav_cls.get_rxcui_from_atc(term)
        # search rxcui by va class code
        elif sterm_type == "va":
            code_lst = rxnav_cls.get_rxcui_from_va(term)
        # search rxcui by string
        elif sterm_type == "string":
            code_lst = rxnav_cls.get_rxcui_from_str(term)
        # search ndc by rxcui
        elif sterm_type == "ndc":
            code_lst = rxnav_cls.get_ndc_from_rxcui(term)
        else:
            print('sterm_type=',sterm_type,' is not a searchable type!')

        dict_agg[term] = code_lst

        # report progress
        if verbose:
            print(f'finish search for rxcui:{term}')

    # write single dictionary to json
    with open(f"{path_to_save}/{filename_to_save}.json","w",encoding='utf-8') as writer: 
        json.dump(dict_agg, writer, ensure_ascii=False, indent=4)

