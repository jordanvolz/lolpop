from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.databricks_sql_data_connector import DatabricksSQLDataConnector


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class DatabricksSQLDataTransformer(BaseDataTransformer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.databricks_config = utils.load_config([
            "DATABRICKS_SERVER_HOST",
            "DATABRICKS_HTTP_PATH",
            "DATABRICKS_TOKEN",
            "DATABRICKS_CATALOG",
            "DATABRICKS_SCHEMA",
            ], self.config)

    def transform(self, sql, *args, **kwargs):
        data = DatabricksSQLDataConnector._load_data(
            sql, self.databricks_config)
        return data
