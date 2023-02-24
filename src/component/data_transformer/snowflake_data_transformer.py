import pandas as pd 
import snowflake.connector as snow_conn

from component.data_transformer.abstract_data_transformer import AbstractDataTransformer
from utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class SnowflakeDataTransformer(AbstractDataTransformer): 
    #use load_config to allow passing these in via env_variables
    #__REQUIRED_CONF__ = {
    #    "config" : ["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"]
    #}

    def __init__(self, conf, pipeline_conf, runner_conf, **kwargs): 
        super().__init__(conf, pipeline_conf, runner_conf, **kwargs)

        self.snowflake_config = utils.load_config([
            "ACCOUNT", 
            "USER", 
            "PASSWORD", 
            "DATABASE", 
            "SCHEMA", 
            "WAREHOUSE"], conf)


    def get_data(self, table, **kwargs):
        sql = "SELECT * FROM %s" %table
        
        data = self._load_data(sql, self.snowflake_config)
        
        return data  

    def transform(self, sql, **kwargs):
        data = self._load_data(sql, self.snowflake_config)

        return data  # last line of the CLI 

    #load data into df
    def _load_data(self, sql, config):
        result = pd.DataFrame() 
        result = get_from_snowflake(
            sql, 
            config.get("ACCOUNT"), 
            config.get("USER"), 
            config.get("PASSWORD"), 
            config.get("DATABASE"), 
            config.get("SCHEMA"), 
            config.get("WAREHOUSE")
            )
        return result

#get df from snowflake
def get_from_snowflake(sql, account, user, password, database, schema, warehouse):
    connection = snow_conn.connect(
        account=account,
        user=user,
        password=password,
        database=database,
        schema=schema,
        warehouse=warehouse,
    )
    cur = connection.cursor()
    cur.execute(sql)
    #coerce_float helps in converting numeric types into floats
    #otherwise they end up as strings and mess stuff up
    df = pd.DataFrame.from_records(
        iter(cur), columns=[x[0] for x in cur.description], coerce_float=True)
    return df
