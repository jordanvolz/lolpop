
from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
from databricks import sql as databricks_sql
from sqlalchemy import create_engine
from tqdm import tqdm

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class DatabricksSQLDataConnector(BaseDataConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.databricks_config = utils.load_config(
            [
                "DATABRICKS_SERVER_HOSTNAME", 
                "DATABRICKS_HTTP_PATH", 
                "DATABRICKS_TOKEN", 
                "DATABRICKS_CATALOG", 
                "DATABRICKS_SCHEMA",
            ]
            , self.config)

    def get_data(self, table, sql=None, *args, **kwargs):
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to DatabricksConnector in order to retrieve data.")

        data = self._load_data(sql, self.databricks_config)

        return data

    def save_data(self, data, table, *args, **kwargs):
        #check if table already exists
        tables = self.get_data(None, sql="SHOW TABLES")

        #if table exists, see if we've added new columns or deleted columns
        table_exists = tables[tables["tableName"] == table].shape[0] > 0
        if table_exists:
           table_schema = self.get_data(table)
           new_features = [x for x in data.columns if x.upper(
           ) not in table_schema.columns.str.upper()]
           deleted_features = [
               x for x in table_schema.columns if x.upper() not in data.columns.str.upper()]

           #if we have new columns, we need to alter the table definiton
           if len(new_features) > 0:
               sql = "ALTER TABLE %s " % (table)
               for col_name in new_features:
                   col_type = data.dtypes[col_name]
                   dbricks_type = self._map_pandas_col_type_to_databrickssql_type(
                       col_type)
                   sql = sql + ("ADD COLUMN %s %s" %
                                (col_name.upper(), dbricks_type))
               self.get_data(None, sql=sql)

           #if we've deleted any features, then just add blank rows to the dataframe
           if len(deleted_features) > 0:
               for feature in deleted_features:
                   data[feature] = None

        #now we can save our data
        self._save_data(data, table, self.databricks_config)

     #load data into df
    @classmethod
    def _load_data(self, sql, config):
        df = pd.DataFrame()
        with databricks_sql.connect(server_hostname=config.get("DATABRICKS_SERVER_HOSTNAME"),
                         http_path=config.get("DATABRICKS_HTTP_PATH"),
                         access_token=config.get("DATABRICKS_TOKEN")) as connection:

            with connection.cursor() as cursor:
                cursor.execute(sql)

                df = pd.DataFrame.from_records(
                    iter(cursor), columns=[x[0] for x in cursor.description], coerce_float=True)

        return df

    def _save_data(self, data, table, config):
        chunksize = 16384 
        catalog = config.get("DATABRICKS_CATALOG", "")
        schema = config.get("DATABRICKS_SCHEMA", "")
        engine = create_engine("databricks://token:%s@%s?http_path=%s&catalog=%s&schema=%s"
                               %(config.get("DATABRICKS_TOKEN"), config.get("DATABRICKS_SERVER_HOSTNAME"), 
                                 config.get("DATABRICKS_HTTP_PATH"), catalog, schema))
        connection = engine.connect()

        with tqdm(total=len(data), desc="Upload to %s.%s.%s" % (catalog, schema, table)) as pbar:
            for i, cdf in enumerate(utils.chunker(data, chunksize)):
                cdf.to_sql(table.replace(" ", "_"), con=engine,
                        index=False, if_exists="append", chunksize=chunksize, method="multi")
                pbar.update(chunksize)
        connection.close()
        engine.dispose()

    def _map_pandas_col_type_to_databrickssql_type(self, col_type):
        """_summary_

        Args:
            col_type (_type_): _description_

        Returns:
            _type_: _description_
        """
        if col_type.kind == 'M':
            # datetime and timestamp columns in pandas are converted to datetime64[ns] dtype, which corresponds to 'TIMESTAMP'
            column_type = 'TIMESTAMP'
        elif col_type.kind == 'm':
            # timedelta columns in pandas are converted to timedelta64[ns] dtype, which corresponds to 'INTERVAL'
            column_type = 'INTERVAL'
        elif col_type.kind == 'b':
            # boolean columns in pandas are converted to 'bool' dtype, which corresponds to 'boolean'
            column_type = 'BOOLEAN'
        elif col_type.kind == 'i' or col_type.kind == "u":
            column_type = 'BIGINT'
        elif col_type.kind == 'f' or col_type.kind == 'c':
            # float columns in pandas are converted to 'float64' dtype, which corresponds to 'DECIMAL'
            column_type = 'DECIMAL'
        else:
            # All other column types in pandas are assumed to be string columns, which correspond to 'STRING'
            column_type = 'STRING'
        return column_type

