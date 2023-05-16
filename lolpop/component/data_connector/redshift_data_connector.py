from lolpop.component.data_connector.postgres_data_connector import PostgresDataConnector
from lolpop.utils import common_utils as utils
@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class RedshiftDataConnector(PostgresDataConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redshift_config = utils.load_config(
            ["REDSHIFT_HOST", "REDSHIFT_PORT", "REDSHIFT_USER", "REDSHIFT_PASSWORD", "REDSHIFT_DBNAME", "REDSHIFT_SCHEMA"], self.config)
        self.pg_config = {k.replace("REDSHIFT", "POSTGRES"):v for k,v in self.redshift_config.items()}
