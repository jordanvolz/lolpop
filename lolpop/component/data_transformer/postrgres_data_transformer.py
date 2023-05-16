from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.postgres_data_connector import PostgresDataConnector


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class PostgresDataTransformer(BaseDataTransformer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pg_config = utils.load_config([
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_DBNAME",
            "POSTGRES_SCHEMA",
        ], self.config)

    def transform(self, sql, *args, **kwargs):
        data = PostgresDataConnector._load_data(
            sql, self.pg_config)
        return data
