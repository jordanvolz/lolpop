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
                    "Table or SQL command must be provided to DuckDBDataTransformer in order to retrieve data.")

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
                    sf_type = self._map_pandas_col_type_to_sf_type(col_type)
                    sql = sql + ("ADD COLUMN %s %s" %
                                 (col_name.upper(), sf_type))
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
        con = duckdb.connect(database = path)

        if not table_exists: 
            con.sql("CREATE TABLE %s as SELECT * from data" %table_name)
        else: 
            con.sql("INSERT INTO %s as SELECT * from data" % table_name)



#save to snowflake