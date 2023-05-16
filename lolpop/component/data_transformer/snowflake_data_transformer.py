from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.snowflake_data_connector import SnowflakeDataConnector

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class SnowflakeDataTransformer(BaseDataTransformer): 

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.snowflake_config = utils.load_config([
            "SNOWFLAKE_ACCOUNT", 
            "SNOWFLAKE_USER", 
            "SNOWFLAKE_PASSWORD", 
            "SNOWFLAKE_DATABASE", 
            "SNOWFLAKE_SCHEMA", 
            "SNOWFLAKE_WAREHOUSE"], self.config)

    def transform(self, sql, *args, **kwargs):
        data = SnowflakeDataConnector._load_data(sql, self.snowflake_config)
        return data 
