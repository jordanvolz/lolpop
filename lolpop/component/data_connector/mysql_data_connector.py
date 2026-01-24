from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from tqdm import tqdm


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MySQLDataConnector(BaseDataConnector):
    __REQUIRED_CONF__ = {"config": ["MYSQL_HOST", "MYSQL_PORT",
                                    "MYSQL_USER", "MYSQL_PASSWORD",
                                    "MYSQL_DBNAME"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mysql_config = utils.load_config(
            ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DBNAME"],
            self.config,
        )

    def get_data(self, table, sql=None, *args, **kwargs):
        """
        Retrieves data from the database.

        Args:
            table (str): name of database table to retrieve data from
            sql (str): SQL query to retrieve data, defaults to None

        Returns:
            pandas.DataFrame: retrieved data
        """
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to MySQLDataConnector in order to retrieve data.")

        data = self._load_data(sql, self.mysql_config)

        return data

    def save_data(self, data, table, *args, **kwargs):
        """
        Saves data to a database table.

        Args:
            data (pandas.DataFrame): data to save to the database
            table (str): name of database table to save data to
        """
        #check if table already exists
        tables = self.get_data(
            None,
            sql=(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = '%s'"
                % self.mysql_config.get("MYSQL_DBNAME")
            ),
        )

        #if table exists, see if we've added new columns or deleted columns
        table_exists = tables[tables["table_name"] == table].shape[0] > 0
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
                    mysql_type = self.__map_pandas_col_type_to_mysql_type(
                        col_type)
                    sql = sql + ("ADD COLUMN %s %s" %
                                 (col_name.upper(), mysql_type))
                self.get_data(None, sql=sql)

            #if we've deleted any features, then just add blank rows to the dataframe
            if len(deleted_features) > 0:
                for feature in deleted_features:
                    data[feature] = None

        #now we can save our data
        self._save_data(data, table, self.mysql_config)

    #load data into df
    @classmethod
    def _load_data(self, sql, config, *args, **kwargs):
        """
        Loads data into a pandas DataFrame object.

        Args:
            sql (str): SQL query to retrieve data
            config (dict): configuration dictionary

        Returns:
            pandas.DataFrame: data from database

        """
        data = pd.DataFrame()

        with self._get_connector(config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

                data = pd.DataFrame.from_records(
                    iter(cursor), columns=[x[0] for x in cursor.description], coerce_float=True)

        return data

    def _save_data(self, data, table, config, *args, **kwargs):
        """
        Saves data to a database table.

        Args:
            data (pandas.DataFrame): data to save to the database
            table (str): name of database table to save data to
            config (dict): configuration dictionary

        """
        chunksize = 16384
        database = config.get("MYSQL_DBNAME", "")
        engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s"
                               % (config.get("MYSQL_USER"), config.get("MYSQL_PASSWORD"),
                                  config.get("MYSQL_HOST"), config.get("MYSQL_PORT"), database))
        connection = engine.connect()
        table_name = table.replace(" ", "_")
        with tqdm(total=len(data), desc="Upload to %s.%s" % (database, table_name)) as pbar:
            for i, cdf in enumerate(utils.chunker(data, chunksize)):
                cdf.to_sql(table_name, con=engine,
                           index=False, if_exists="append", chunksize=chunksize, method="multi")
                pbar.update(chunksize)
        connection.close()
        engine.dispose()

    def __map_pandas_col_type_to_mysql_type(self, col_type):
        """_summary_

        Maps column data types from pandas to MySQL.

        Args:
            col_type (pd.dtype): pandas data type

        Returns:
            str: corresponding data type for MySQL
        """
        if col_type.kind == 'M':
            # datetime and timestamp columns in pandas are converted to datetime64[ns] dtype, which corresponds to 'DATETIME'
            column_type = 'DATETIME'
        elif col_type.kind == 'm':
            # timedelta columns in pandas are converted to timedelta64[ns] dtype
            column_type = 'BIGINT'
        elif col_type.kind == 'b':
            # boolean columns in pandas are converted to 'bool' dtype, which corresponds to 'BOOLEAN'
            column_type = 'BOOLEAN'
        elif col_type.kind == 'i' or col_type.kind == "u":
            column_type = 'BIGINT'
        elif col_type.kind == 'f' or col_type.kind == 'c':
            # float columns in pandas are converted to 'float64' dtype, which corresponds to 'double'
            column_type = 'DOUBLE'
        else:
            # All other column types in pandas are assumed to be string columns, which correspond to 'text' in MySQL
            column_type = 'TEXT'
        return column_type

    @staticmethod
    def _get_connector(config):
        conn = pymysql.connect(
            host=config.get("MYSQL_HOST"),
            port=config.get("MYSQL_PORT"),
            user=config.get("MYSQL_USER"),
            password=config.get("MYSQL_PASSWORD"),
            database=config.get("MYSQL_DBNAME"),
        )

        return conn
