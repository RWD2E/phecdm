# Kor!
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

# LangChain Models
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# Standard Helpers
import pandas as pd
import requests
import time
import json
from datetime import datetime
import os

# Text Helpers
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# For token counting
from langchain.callbacks import get_openai_callback

# Some Helper functions
def get_access_info(path_to_key=None):
    # populate default location for config file
    if path_to_key is None:
        path_to_key = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\.config\config.json'    
    # load config file
    with open(path_to_key) as config_file:
        key = json.load(config_file)
    return(key)

def printOutput(output):
    print(json.dumps(output,sort_keys=True, indent=3))

# create LLM object
openai_api_key = get_access_info()['openai-api']['api-key']
llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature = 0,
    # max_token = 200,
    openai_api_key=openai_api_key
)

unit_schema_many = Object(
    id="in_dose_unit",
    description="The raw string about dose and unit for a drug",
    examples=[
        ("losartan/hydrochlorothiazide 100mg-25mg tablet", 
        [
            {"in":"losartan", "dose":100, "units": "mg"},
            {"in":"hydrochlorothiazide", "dose":25, "unit":"mg"}
        ]),
        ("CALCIUM CARB/VIT D3/MINERALS 600 MG-400", 
        [
            {"in":"CALCIUM CARB", "dose":600, "units": "mg"},
            {"in":"VIT D3","dose":400, "unit":"mg"}
        ]),

    ],
    attributes=[
        Text(
            id="in",
            description="The name of the ingredient."
        ),
        Number(
            id="dose",
            description="The per-unit dose quantity."
        ),
        Text(
            id="unit",
            description="The dose unit for the drug"
        ),
    ],
    many = True
)

# test_text = "budesonide/formoterol fumarate 160-4.5MCG"
# chain = create_extraction_chain(llm, unit_schema_many, encoder_or_encoder_class="json")
# output = chain.run(text=test_text)['data']
# printOutput(output)

# get source valuset - stored csv
src_file_loc = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\/res\/valueset_autogen\pde-dose-unit.csv'    
src_vs = pd.read_csv(src_file_loc)

# create a small sample
src_vs_sample = src_vs.sample(n = 30)

# loop over the source concept list 
mapping_output = list()
for index, row in src_vs_sample.iterrows():
    chain = create_extraction_chain(llm, unit_schema_many, encoder_or_encoder_class="json")
    output = chain.run(text=row['DRUG_UNIT_STR'])['data']
    output['raw_str'] = row['DRUG_UNIT_STR']
    mapping_output.append(output)
    # report progress
    print(f"{row['DRUG_UNIT_STR']} parsed!")

# save json file
tgt_file_loc = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\/res\/valueset_autogen\pde-dose-unit-parsed.json'
with open(tgt_file_loc, 'w') as json_file:
    json.dump(mapping_output, json_file, indent=4)

# # get target/reference valueset - from url
# url = 
# resp = requests.get(url)
# resp_df = pd.read_excel(resp.content,sheet_name="UNIT")

# # fuzzy string match to map each source value to the closest target value



# output mapping table


