import json
import requests
import api_call_utils as apiutil
import api_get_umls as apiumls

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

    def get_rxcui_all(self,rxcui,tty_lst=['SCD','SCDC','SCDF','SCDG','SBD','SBDC','SBDF','SBDG']):
        '''
        rxnav API call to collect all levels of RXCUI
        https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getAllRelatedInfo.html
        '''
        # time.sleep(0.05)
        response = requests.get(f'{self.API_URI}/rxcui/{rxcui}/allrelated.json')
        results = json.loads(response.text)
        all_medications = []
        for group in results['allRelatedGroup']['conceptGroup']:
            if 'conceptProperties' in group and group['tty'] in tty_lst:
                rxcui_add = group['conceptProperties'][0]
                rxcui_add['ndc'] = self.get_ndc_from_rxcui(rxcui_add['rxcui'])
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
        for candidate in results['approximateGroup']['candidate']:
            if int(candidate['rank']) <= keep_rk and candidate['rxcui'] not in rxcui_candidates:
                # when term only contains ingredient string, the results are often rxcui at ingredient level
                rxcui_candidates.append(candidate['rxcui'])

        # Loop through rxcui_candidates 
        rxcui_lst = []
        for ing in rxcui_candidates:
            allrelacodes = self.get_rxcui_all(ing,tty_lst=['SCD','SCDC','SBD','SBDC'])
            rxcui_lst.extend(allrelacodes)

        # Save to a csv file
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
            allrelacodes = self.get_rxcui_all(ing['rxcui'],tty_lst=['SCD','SCDC','SBD','SBDC'])
            ing['allrelacodes'] = allrelacodes
            rxcui_lst.append(ing)

        # Save to a csv file
        return(rxcui_lst)      

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
        # search rxcui by atc
        elif sterm_type == "atc":
            code_lst = rxnav_cls.get_rxcui_from_atc(term)
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

