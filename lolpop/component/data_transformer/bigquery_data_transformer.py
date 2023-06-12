from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.bigquery_data_connector import BigQueryDataConnector

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class BigQueryDataTransformer(BaseDataTransformer): 


    __REQUIRED_CONF__ = {
        "config": ["GOOGLE_PROJECT", "GOOGLE_DATASET"]
    }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.bigquery_config = utils.load_config(
            ["GOOGLE_KEYFILE", "GOOGLE_PROJECT", "GOOGLE_DATASET"], self.config)

    def transform(self, sql, *args, **kwargs):
        """
        Transforms data using BigQueryDataConnector and returns the transformed data.

        Args:
            sql (str): The SQL query to be executed in BigQuery.

        Returns:
            The transformed data returned by the BigQueryDataConnector._load_data method.
        """
        data = BigQueryDataConnector._load_data(sql, self.bigquery_config)
        return data 
