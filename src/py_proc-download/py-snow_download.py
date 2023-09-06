##TODO!

# Snowflake helper functions
import json
from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

# Some Helper functions
def get_access_info(path_to_key=None):
    # populate default location for config file
    if path_to_key is None:
        path_to_key = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\.config\config.json'    
    # load config file
    with open(path_to_key) as config_file:
        key = json.load(config_file)
    return(key)

# make snowflake connection
sf_config = get_access_info()['snowflake-api']
connection_params = {
    "account":sf_config["account"],
    "user":sf_config["user"],
    "password":sf_config["password"],
    "role":sf_config["role"],
    "warehouse":sf_config["warehouse"],
    "database":sf_config["database"]
}
new_session = Session.builder.configs(connection_params).create()  

# register a named temporary stored procedure
@sproc(name="get_partd_unit",is_permanent=True,packages=["snowflake-snowpark-python"])
def get_partd_unit(session: snowflake.snowpark.Session,schema_lst) ->dict:
    for schema in schema_lst:
        session.sql(f"select unique UNIT from {schema}.")




# close session
# new_session.close()