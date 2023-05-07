from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from lolpop.component.data_connector.duckdb_data_connector import DuckDBDataConnector


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class DuckDBDataTransformer(BaseDataTransformer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self._get_config("duckdb_path")

    def transform(self, sql, *args, **kwargs):
        data = DuckDBDataConnector._load_data(sql, self.path)
        return data
