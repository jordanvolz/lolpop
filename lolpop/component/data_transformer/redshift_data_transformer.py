from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.redshift_data_connector import RedshiftDataConnector


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class RedshiftDataTransformer(BaseDataTransformer):

    __REQUIRED_CONF__ = {"config": ["REDSHIFT_HOST",
                                    "REDSHIFT_PORT",
                                    "REDSHIFT_USER",
                                    "REDSHIFT_PASSWORD",
                                    "REDSHIFT_DBNAME",
                                    "REDSHIFT_SCHEMA"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redshift_config = utils.load_config([
            "REDSHIFT_HOST",
            "REDSHIFT_PORT",
            "REDSHIFT_USER",
            "REDSHIFT_PASSWORD",
            "REDSHIFT_DBNAME",
            "REDSHIFT_SCHEMA",
        ], self.config)
        self.pg_config = {
            k.replace("REDSHIFT", "POSTGRES"): v for k, v in self.redshift_config.items()}

    def transform(self, sql, *args, **kwargs):
        """
        Retrieves data from a RedshiftDataConnector object based on SQL provided

        Args:
            sql (str): SQL query to retrieve data from the database
        Returns:
            data (pandas dataframe): A pandas dataframe containing the data retrieved from the Redshift database
        """
        data = RedshiftDataConnector._load_data(
            sql, self.pg_config)
        return data
