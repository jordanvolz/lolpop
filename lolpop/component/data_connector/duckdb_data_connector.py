from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
import duckdb

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class DuckDBDataConnector(BaseDataConnector):
    __REQUIRED_CONF__ = {"config": ["duckdb_path"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self._get_config("duckdb_path")

    def get_data(self, table, sql=None, *args, **kwargs):
        """
        Retrieves data from the DuckDBDataConnector table or custom SQL provided and returns in a pandas dataframe.

        Args:
            table (str): Name of the table to retrieve data from.
            sql (str): The optional SQL query to execute. Default value is None.

        Returns:
            data: Pandas dataframe object containing the data.

        Raises:
            Exception: If both table and sql statement are not provided.
        """
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to DuckDBDataConnector in order to retrieve data.")

        data = self._load_data(sql, self.path)

        return data

    def save_data(self, data, table, *args, **kwargs):
        """
        Saves data to the specified table in the specified DuckDBDataConnector instance.
        If the table does not exist, it gets created with the data structure from the dataframe provided.
        If a column is missing, it adds the column as nulls. This preserves the structure of the destination table.

        Args:
            data (pandas.DataFrame): Pandas dataframe containing the data to be saved.
            table (str): Name of the table to save the data to.

        """
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
                    duckdb_type = self.__map_pandas_col_type_to_duckdb_type(col_type)
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
    def _load_data(self, sql, path, *args, **kwargs):
        """
        Loads data into a pandas dataframe.
        
        Args:
            sql (str): SQL query to execute to fetch data.
            path (str): Path to database.
        
        Returns:
            result: Pandas dataframe object containing the data from the query.
        """
        result = pd.DataFrame()
        with duckdb.connect(database = path) as con: 
            res = con.sql(sql)
            result = res.df() 
        return result

    def _save_data(self, data, table_name, path, table_exists, *args, **kwargs):
        """
        Saves data into the DuckDBDataConnector table.
        
        Args:
            data (pd.DataFrame): Pandas dataframe object containing data.
            table_name (str): Name of the table.
            path (str): Path to database.
            table_exists (bool): Check if the table exists or not.
        
        Returns: 
            None

        """
        if data is not None and len(data)>0: 
            with duckdb.connect(database = path) as con: 
                if not table_exists: 
                    con.sql("CREATE TABLE %s as SELECT * from data" %table_name)
                else: 
                    con.sql("INSERT INTO %s SELECT * from data" % table_name)


    def __map_pandas_col_type_to_duckdb_type(self, col_type):
        """
        This is a private method. It maps pandas data types to duckdb data types.
        
        Args:
            col_type (pd.dtype): Pandas data type.

        Returns:
            column_type: DuckDB data type corresponding to pandas data type.

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
