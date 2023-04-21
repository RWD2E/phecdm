## https://www.nlm.nih.gov/vsac/support/usingvsac/vsacsvsapiv2.html
## https://github.com/HHS/uts-rest-api/blob/master/samples/python/retrieve-value-set-info.py

import requests
import xmltodict
import json
import pandas as pd
import api_call_utils as apiutil
import time

class VsacSearch:
    '''
    search VSAC API and return requested results in human-readable format
    '''
    # global values
    AUTH_URI = apiutil.get_access_info()['uts-auth-api']['auth-uri']
    TGT_ENDPOINT = apiutil.get_access_info()['uts-auth-api']['auth-endpoint']
    ST_ENDPOINT = apiutil.get_access_info()['uts-auth-api']['service-endpoint']
    API_KEY = apiutil.get_access_info()['uts-auth-api']['api-key']
    API_BURI = apiutil.get_access_info()['umls-api']['vsac-svs-endpoint']
    # instance value
    # basic authentication using UMLS API key
    def __init__(self):
        self.authclient = apiutil.two_factor_auth(self.AUTH_URI,self.TGT_ENDPOINT,self.ST_ENDPOINT,self.API_KEY)
        self.tgt = self.authclient.get_tgt()
        self.tkt = self.authclient.get_st(self.tgt, verbose=False)

    # main function for getting code list of specified vocab
    def get_cd_from_oid_svs(self,oid) -> dict:
        '''
        get valueset details
        '''
        # time.sleep(0.05)
        # build search query
        query = {
            'id': oid, 
            'ticket': self.tkt
        }
        
        # https://www.nlm.nih.gov/vsac/support/usingvsac/svsapiendpoints/mostrecentexpansion.html
        r = requests.get(f'{self.API_BURI}/RetrieveValueSet',query)      
        xml_dict = xmltodict.parse(r.content)
        display = xml_dict['ns0:RetrieveValueSetResponse']['ns0:ValueSet']['@displayName']
        vs_lst = xml_dict['ns0:RetrieveValueSetResponse']['ns0:ValueSet']['ns0:ConceptList']['ns0:Concept']

        # collect result
        out = {
            "oid":oid,
            "displayName":display,
            "vs":vs_lst}
        
        return out

def batch_write_rx_code_json(
    path_to_save, #absolute path,
    filename_to_save,
    sterms:list,
    verbose=True
):
    '''
    extract valueset with controlled terminology from VSAC
    '''     
    # collect aggregated dict
    lst_dict = []
    for oid in sterms:
        # get valueset list
        vsac_cls = VsacSearch()
        dict_oid = vsac_cls.get_cd_from_oid_svs(oid)
        # append
        lst_dict.append(dict_oid) 
        # report progress
        if verbose:
            print(f"Finish search for term:{oid}:{dict_oid['displayName']}")
            
    # write single dictionary to json
    with open(f"{path_to_save}/{filename_to_save}.json","w",encoding='utf-8') as writer: 
        json.dump(lst_dict, writer, ensure_ascii=False, indent=4)


