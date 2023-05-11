from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
import duckdb

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class DuckDBDataConnector(BaseDataConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self._get_config("duckdb_path")

    def get_data(self, table, sql=None, *args, **kwargs):
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to DuckDBDataConnector in order to retrieve data.")

        data = self._load_data(sql, self.path)

        return data

    def save_data(self, data, table, *args, **kwargs):
        #check if table already exists
        tables = self.get_data(None, sql="SHOW TABLES")

        #if table exists, see if we've added new columns or deleted columns
        table_exists = tables[tables["name"]==table].shape[0] > 0
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
                    duckdb_type = self._map_pandas_col_type_to_duckdb_type(col_type)
                    sql = sql + ("ADD COLUMN %s %s" %
                                 (col_name.upper(), duckdb_type))
               self.get_data(None, sql=sql)

           #if we've deleted any features, then just add blank rows to the dataframe
           if len(deleted_features) > 0:
               for feature in deleted_features:
                   data[feature] = None

        #now we can save our data
        self._save_data(data, table, self.path, table_exists)

     #load data into df
    @classmethod
    def _load_data(self, sql, path):
        result = pd.DataFrame()
        with duckdb.connect(database = path) as con: 
            res = con.sql(sql)
            result = res.df() 
        return result

    def _save_data(self, data, table_name, path, table_exists):
        with duckdb.connect(database = path) as con: 
            if not table_exists: 
                con.sql("CREATE TABLE %s as SELECT * from data" %table_name)
            else: 
                con.sql("INSERT INTO %s as SELECT * from data" % table_name)


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
        elif col_type.kind == 'i': 
            column_type = 'BIGINT'
        elif col_type.kind == 'u':
            column_type = 'UBIGINT'
        elif col_type.kind == 'f' or col_type.kind == 'c':
            # float columns in pandas are converted to 'float64' dtype, which corresponds to 'float'
            column_type = 'FLOAT'
        else:
            # All other column types in pandas are assumed to be string columns, which correspond to 'varchar' in Snowflake
            column_type = 'VARCHAR'
        return column_type
