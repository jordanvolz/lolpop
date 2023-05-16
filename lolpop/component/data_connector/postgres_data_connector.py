from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
import psycopg2
from sqlalchemy import create_engine 
import tqdm


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class PostgresDataConnector(BaseDataConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pg_config = utils.load_config(["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DBNAME", "POSTGRES_SCHEMA"], self.config)

    def get_data(self, table, sql=None, *args, **kwargs):
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to DuckDBDataConnector in order to retrieve data.")

        data = self._load_data(sql, self.pg_config)

        return data

    def save_data(self, data, table, *args, **kwargs):
        #check if table already exists
        tables = self.get_data(None, sql="select * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")

        #if table exists, see if we've added new columns or deleted columns
        table_exists = tables[tables["tablename"] == table].shape[0] > 0
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
                   pg_type = self._map_pandas_col_type_to_pg_type(
                       col_type)
                   sql = sql + ("ADD COLUMN %s %s" %
                                (col_name.upper(), pg_type))
               self.get_data(None, sql=sql)

           #if we've deleted any features, then just add blank rows to the dataframe
           if len(deleted_features) > 0:
               for feature in deleted_features:
                   data[feature] = None

        #now we can save our data
        self._save_data(data, table, self.pg_config)

    #load data into df
    @classmethod
    def _load_data(self, sql, config):
        data = pd.DataFrame()

        with self._get_connector(config) as connection: 
            with connection.cursor() as cursor:
                cursor.execute(sql)

                data = pd.DataFrame.from_records(
                    iter(cursor), columns=[x[0] for x in cursor.description], coerce_float=True)

        return data

    def _save_data(self, data, table, config):
        chunksize = 16384 
        database = config.get("POSTGRES_DBNAME", "")
        engine = create_engine("postgresql://%s:%s@%s:%s/%s"
                               % (config.get("POSTGRES_USER"), config.get("POSTGRES_PASSWORD"),
                                  config.get("POSTGRES_HOST"), config.get("POSTGRES_PORT"), database))
        connection = engine.connect()
        table_name = "%s.%s" % (table.replace(" ", "_"), config.get("POSTGRES_SCHEMA"))
        with tqdm(total=len(data), desc="Upload to %s.%s" % (database, table_name)) as pbar:
            for i, cdf in enumerate(utils.chunker(data, chunksize)):
                cdf.to_sql(table_name, con=engine,
                           index=False, if_exists="append", chunksize=chunksize, method="multi")
                pbar.update(chunksize)
        connection.close()
        engine.dispose()

    def _map_pandas_col_type_to_duckdb_type(self, col_type):
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
            # float columns in pandas are converted to 'float64' dtype, which corresponds to 'float'
            column_type = 'FLOAT8'
        else:
            # All other column types in pandas are assumed to be string columns, which correspond to 'varchar' in Snowflake
            column_type = 'TEXT'
        return column_type
    
    def _get_connector(config): 
        conn=psycopg2.connect(
            host=config.get("POSTGRES_HOST"),
            port=config.get("POSTGRES_PORT"),
            user=config.get("POSTGRES_USER"),
            password=config.get("POSTGRES_PASSWORD"),
            dbname=config.get("POSTGRES_DBNAME"),
        )

        return conn 

