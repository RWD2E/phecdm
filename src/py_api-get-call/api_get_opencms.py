## https://data.cms.gov/search

import requests
import json
import os
import pandas as pd
import api_call_utils as apiutil
from flatten_json import flatten

# which_cms_open_data = "provider_taxonomy-endpoint"
# search_params = {

# }

which_cms_open_data = "npi-registry-endpoint"
search_params = {
    "number":'',
    "enumeration_type":'2',
    "taxonomy_description":'',
    "name_purpose":'',
    "first_name":'',
    "use_first_name_alias":True,
    "last_name":'',
    "organization_name":'',
    "address_purpose":'',
    "city":'',
    "state":'',
    "postal_code":'33136',
    "country_code":'',
    "limit":200,
    "skip":'',
    "pretty":False,
    "version":2.1
}

# make api request
url = apiutil.get_access_info()['cmsdata-api'][which_cms_open_data]
par_str = '&'.join([f'{key}={value}' for key, value in search_params.items()])
response_api = requests.get(f'{url}/?{par_str}')
print(f'status_code:{response_api.status_code}')

# convert json to dataframe
rslt_json = response_api.json()
result_count = rslt_json['result_count']
print(result_count)
#Create loop parameters
i = 0
#Create loop
while i < result_count:
    record = flatten(rslt_json['results'][i])
    print(record)
    data = pd.DataFrame.from_dict(record,orient='index').T
    if i == 0:
        df = data
    else:
        df = pd.concat([df,data], axis=0, ignore_index=True)
    i+=1



# write to csv file
# path_to_save = f'{os.path.dirname(os.path.dirname(__file__))}/valueset_autogen'
# df.to_csv(f'{path_to_save}/{which_cms_open_data}.csv', index = None)

