from component.data_transformer.abstract_data_transformer import AbstractDataTransformer
from utils import common_utils as utils

import pandas as pd
import snowflake.connector as snow_conn
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from tqdm import tqdm

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


    def get_data(self, table, *args, **kwargs):
        sql = "SELECT * FROM %s" %table
        
        data = self._load_data(sql, self.snowflake_config)
        
        return data  

    def transform(self, sql, *args, **kwargs):
        data = self._load_data(sql, self.snowflake_config)

        return data 

    def save_data(self, data, *args, **kwargs): 
        pass

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
    
    def _save_data(self, data, table_name, config): 
        save_to_snowflake(
            data, 
            table_name,
            config.get("ACCOUNT"),
            config.get("USER"),
            config.get("PASSWORD"),
            config.get("DATABASE"),
            config.get("SCHEMA"),
            config.get("WAREHOUSE")
        )

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

#save to snowflake
def save_to_snowflake(df, table_name, account, user, password, database, schema, warehouse):
	chunksize = 16384  # maximum allowed by snowflake
	engine = create_engine(URL(
		account=account,
		user=user,
		password=password,
		database=database,
		schema=schema,
		warehouse=warehouse,
	))
	connection = engine.connect()
	df = df.rename(columns=str.lower)
	with tqdm(total=len(df), desc="Upload to %s.%s.%s" % (database, schema, table_name)) as pbar:
		for i, cdf in enumerate(chunker(df, chunksize)):
			cdf.to_sql(table_name.replace(" ", "_").upper(), con=engine,
			           index=False, if_exists="append", chunksize=chunksize)
			pbar.update(chunksize)
	connection.close()
	engine.dispose()
