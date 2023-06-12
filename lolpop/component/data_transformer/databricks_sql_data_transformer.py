from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.databricks_sql_data_connector import DatabricksSQLDataConnector


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class DatabricksSQLDataTransformer(BaseDataTransformer):

    __REQUIRED_CONF__ = {"config": ["DATABRICKS_SERVER_HOSTNAME",
                                "DATABRICKS_HTTP_PATH",
                                "DATABRICKS_CATALOG",
                                "DATABRICKS_SCHEMA"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.databricks_config = utils.load_config([
            "DATABRICKS_SERVER_HOSTNAME",
            "DATABRICKS_HTTP_PATH",
            "DATABRICKS_TOKEN",
            "DATABRICKS_CATALOG",
            "DATABRICKS_SCHEMA",
            ], self.config)

    def transform(self, sql, *args, **kwargs):
        """
        Transforms data from a Databricks SQL data source.

        Args:
            sql (str): A SQL statement for querying the Databricks data source.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            data (pandas.DataFrame): A DataFrame of transformed data.

        """
        data = DatabricksSQLDataConnector._load_data(
            sql, self.databricks_config)
        return data
