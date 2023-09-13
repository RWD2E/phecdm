
import os
import openai
import json
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import requests

# Some Helper functions
def get_access_info(path_to_key=None):
    # populate default location for config file
    if path_to_key is None:
        path_to_key = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\.config\config.json'    
    # load config file
    with open(path_to_key) as config_file:
        key = json.load(config_file)
    return(key)

openai.api_key = get_access_info()['openai-api']['api-key']
def get_embedding(text):
    result = openai.Embedding.create(
      model='text-embedding-ada-002',
      input=text
    )
    return result["data"][0]["embedding"]

# test=get_embedding("HFA AEROSOL WITH ADAPTER (GRAM)")
# print(test)

def fuzzy_match(
        src_df, 
        key_col,
        ref_df, 
        ref_col, 
        return_col,
        drop_aux = True,
        threshold=0.85
):
    """
    Function to return semantic similar value from "return_col" by 
    performing fuzzy matching between src_df[ke_col] and ref_df[ref_col]
    """

    src_df_matched = src_df

    src_df['embeddings'] = src_df[key_col].apply(get_embedding)
    ref_df['embeddings'] = ref_df[ref_col].apply(get_embedding)

    nn = NearestNeighbors(n_neighbors=1, metric='cosine').fit(ref_df['embeddings'].to_list())
    distances, indices = nn.kneighbors(src_df['embeddings'].to_list(), return_distance=True)

    src_df_matched[return_col] = [ref_df.loc[indices[i,0], return_col] for i in range(src_df.shape[0])]
    src_df_matched = src_df_matched.merge(ref_df[[return_col,ref_col]], on=return_col)
    src_df_matched['similarity'] = 1 - distances

    if drop_aux:
        src_df_matched.drop(
            columns = ["embeddings","similarity"], 
            inplace=True
        )

    return src_df_matched

# get source valueset - from url
dir_path = 'C:/repos/GROUSE/'
src_df = pd.read_csv(f"{dir_path}/ref/raw/pde-gcdf-raw.csv")

# get reference valueset - from url
resp = requests.get('https://pcornet.org/wp-content/uploads/2023/04/2023_04_03_PCORnet_CDM_ValueSet_ReferenceFile_v1.13.xlsx')
dose_form_ref = pd.read_excel(resp.content,sheet_name="DOSE_FORM")
route_ref = pd.read_excel(resp.content,sheet_name="ROUTE")

# start matching process
dose_form_match = fuzzy_match(
        src_df = src_df, 
        key_col = "GCDF_DESC",
        ref_df = dose_form_ref, 
        ref_col = "DESCRIPTIVE_TEXT", 
        return_col = "CODE",
        threshold=0.5
)
print(dose_form_match)

route_match = fuzzy_match(
        src_df = src_df, 
        key_col = "GCDF_DESC",
        ref_df = route_ref, 
        ref_col = "DESCRIPTIVE_TEXT", 
        return_col = "CODE",
        threshold=0.5
)
print(route_match)

# save as csv
dose_form_match=dose_form_match.rename(columns={"CODE":"CDM_DOSE_FORM","DESCRIPTIVE_TEXT":"CDM_DOSE_FORM_LABEL"})
route_match=route_match.rename(columns={"CODE":"CDM_ROUTE","DESCRIPTIVE_TEXT":"CDM_DOSE_FORM_LABEL"})
output = pd.merge(dose_form_match,route_match,on = ["GCDF","GCDF_DESC"])
tgt_file_loc = dir_path + '/ref/GCDF2FORMROUTE.csv'
output.to_csv(tgt_file_loc, index=False, mode='w')