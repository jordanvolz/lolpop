from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
import snowflake.connector as snow_conn
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from tqdm import tqdm


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class SnowflakeDataConnector(BaseDataConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snowflake_config = utils.load_config([
            "SNOWFLAKE_ACCOUNT",
            "SNOWFLAKE_USER",
            "SNOWFLAKE_PASSWORD",
            "SNOWFLAKE_DATABASE",
            "SNOWFLAKE_SCHEMA",
            "SNOWFLAKE_WAREHOUSE"], self.config)

    def get_data(self, table, sql=None, *args, **kwargs):
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to SnowflakeDataTransformer in order to retrieve data.")

        data = self._load_data(sql, self.snowflake_config)

        return data

    def save_data(self, data, table, *args, **kwargs):
        """_summary_

        Args:
            data (_type_): _description_
            table (_type_): _description_
        """
        #check if table already exists
        tables = self.get_data(None, sql="SHOW TABLES like '%s'" % table)

        #if table exists, see if we've added new columns or deleted columns
        if tables.shape[0] > 0:
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
        self._save_data(data, table, self.snowflake_config)

    def _map_pandas_col_type_to_sf_type(self, col_type):
        """_summary_

        Args:
            col_type (_type_): _description_

        Returns:
            _type_: _description_
        """
        if col_type.kind == 'M':
            # datetime and timestamp columns in pandas are converted to datetime64[ns] dtype, which corresponds to 'datetime64' in Snowflake
            column_type = 'DATETIME'
        elif col_type.kind == 'm':
            # timedelta columns in pandas are converted to timedelta64[ns] dtype, which corresponds to 'variant' in Snowflake
            column_type = 'VARIANT'
        elif col_type.kind == 'b':
            # boolean columns in pandas are converted to 'bool' dtype, which corresponds to 'boolean' in Snowflake
            column_type = 'BOOLEAN'
        elif col_type.kind == 'i' or col_type.kind == 'u':
            # integer columns in pandas are converted to 'int64' dtype, which corresponds to 'integer' in Snowflake
            column_type = 'INTEGER'
        elif col_type.kind == 'f' or col_type.kind == 'c':
            # float columns in pandas are converted to 'float64' dtype, which corresponds to 'float' in Snowflake
            column_type = 'FLOAT'
        else:
            # All other column types in pandas are assumed to be string columns, which correspond to 'varchar' in Snowflake
            column_type = 'VARCHAR'
        return column_type

    #load data into df
    @classmethod
    def _load_data(self, sql, config):
        result = pd.DataFrame()
        result = get_from_snowflake(
            sql,
            config.get("SNOWFLAKE_ACCOUNT"),
            config.get("SNOWFLAKE_USER"),
            config.get("SNOWFLAKE_PASSWORD"),
            config.get("SNOWFLAKE_DATABASE"),
            config.get("SNOWFLAKE_SCHEMA"),
            config.get("SNOWFLAKE_WAREHOUSE")
        )
        return result

    def _save_data(self, data, table_name, config):
        save_to_snowflake(
            data,
            table_name,
            config.get("SNOWFLAKE_ACCOUNT"),
            config.get("SNOWFLAKE_USER"),
            config.get("SNOWFLAKE_PASSWORD"),
            config.get("SNOWFLAKE_DATABASE"),
            config.get("SNOWFLAKE_SCHEMA"),
            config.get("SNOWFLAKE_WAREHOUSE")
        )

#get df from snowflake


def get_from_snowflake(sql, account, user, password, database, schema, warehouse):
    connection = snow_conn.connect(
        account=account,
        user=user,
        password=password,
        database=database,
        schema=schema,
        warehouse=warehouse,
    )
    cur = connection.cursor()
    cur.execute(sql)
    #coerce_float helps in converting numeric types into floats
    #otherwise they end up as strings and mess stuff up
    df = pd.DataFrame.from_records(
        iter(cur), columns=[x[0] for x in cur.description], coerce_float=True)
    
    connection.close()
    
    return df

#save to snowflake


def save_to_snowflake(df, table_name, account, user, password, database, schema, warehouse):
    chunksize = 16384  # maximum allowed by snowflake
    engine = create_engine(URL(
        account=account,
        user=user,
        password=password,
        database=database,
        schema=schema,
        warehouse=warehouse,
    ))
    connection = engine.connect()
    df = df.rename(columns=str.upper)
    with tqdm(total=len(df), desc="Upload to %s.%s.%s" % (database, schema, table_name)) as pbar:
        for i, cdf in enumerate(utils.chunker(df, chunksize)):
            cdf.to_sql(table_name.replace(" ", "_").upper(), con=engine,
                        index=False, if_exists="append", chunksize=chunksize,
                        method=snow_conn.pandas_tools.pd_writer)
            pbar.update(chunksize)
    connection.close()
    engine.dispose()

