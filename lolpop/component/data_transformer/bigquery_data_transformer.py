from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.bigquery_data_connector import BigQueryDataConnector

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class BigQueryDataTransformer(BaseDataTransformer): 

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.bigquery_config = utils.load_config(
            ["GOOGLE_KEYFILE", "GOOGLE_PROJECT", "GOOGLE_DATASET"], self.config)

    def transform(self, sql, *args, **kwargs):
        data = BigQueryDataConnector._load_data(sql, self.bigquery_config)
        return data 
