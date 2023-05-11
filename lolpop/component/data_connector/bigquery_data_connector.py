from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

import os 

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class BigQueryDataConnector(BaseDataConnector):
    __REQUIRED_CONF__ = {"config": ["GOOGLE_PROJECT"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bigquery_config = utils.load_config(
            ["GOOGLE_KEYFILE", "GOOGLE_PROJECT", "GOOGLE_DATASET"], self.config)
  

    def get_data(self, table, sql=None, *args, **kwargs):
        if sql is None:
            if table is not None:
                sql = "SELECT * FROM %s" % table
            else:
                raise Exception(
                    "Table or SQL command must be provided to BigQueryDataTransformer in order to retrieve data.")

        data = self._load_data(sql, self.bigquery_config)

        return data

    def save_data(self, data, table, *args, **kwargs):
        """_summary_

        Args:
            data (_type_): _description_
            table (_type_): _description_
        """
        #check if table already exists
        sql = "SELECT * FROM %s.INFORMATION_SCHEMA.TABLES" %self.bigquery_config.get("GOOGLE_DATASET")
        tables = self.get_data(None, sql=sql)

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
                    bq_type = self._map_pandas_col_type_to_bq_type(col_type)
                    sql = sql + ("ADD COLUMN %s %s" %
                                 (col_name.upper(), bq_type))
               self.get_data(None, sql=sql)

           #if we've deleted any features, then just add blank rows to the dataframe
           if len(deleted_features) > 0:
               for feature in deleted_features:
                   data[feature] = None

        #now we can save our data
        self._save_data(data, table, self.bigquery_config)

    def _map_pandas_col_type_to_bg_type(self, col_type):
        """_summary_

        Args:
            col_type (_type_): _description_

        Returns:
            _type_: _description_
        """
        if col_type.kind == 'M':
            # datetime and timestamp columns in pandas are converted to datetime64[ns] dtype, which corresponds to 'datetime64'
            column_type = 'DATETIME'
        elif col_type.kind == 'm':
            # timedelta columns in pandas are converted to timedelta64[ns] dtype, which corresponds to 'variant'
            column_type = 'INTERVAL'
        elif col_type.kind == 'b':
            # boolean columns in pandas are converted to 'bool' dtype, which corresponds to 'boolean'
            column_type = 'BOOL'
        elif col_type.kind == 'i' or col_type.kind == 'u':
            # integer columns in pandas are converted to 'int64' dtype, which corresponds to 'integer'
            column_type = 'INT64'
        elif col_type.kind == 'f' or col_type.kind == 'c':
            # float columns in pandas are converted to 'float64' dtype, which corresponds to 'float'
            column_type = 'FLOAT64'
        else:
            # All other column types in pandas are assumed to be string columns, which correspond to 'varchar'
            column_type = 'STRING'
        return column_type

    #load data into df
    @classmethod
    def _load_data(self, sql, config):
        result = pd.DataFrame()
        client = self._get_client(config.get("GOOGLE_KEYFILE"), project=config.get("GOOGLE_PROJECT"))

        # Run a query to retrieve data from the table
        query = client.query(sql)

        # Get the results of the query as a Pandas DataFrame
        result = query.to_dataframe()

        return result

    def _save_data(self, data, table_name, config):
        # Set up the BigQuery client
        client = client = self._get_client(config.get(
            "GOOGLE_KEYFILE"), project=config.get("GOOGLE_PROJECT"))

        # Set up the table reference
        dataset = client.dataset(config.get("GOOGLE_DATASET"))
        table = dataset.table(table_name)

        # Upload the DataFrame to BigQuery
        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        load_job = client.load_table_from_dataframe(data, table, job_config=job_config)

        # Wait for the job to complete
        try: 
            load_job.result()
            self.log("Successfully uploaded table %s to dataset %s" %
                     (table, config.get("GOOGLE_DATASET")))
        except Exception as e:
            self.log("Failed to upload table %s to dataset %s: %s" % 
                     (table, config.get("GOOGLE_DATASET"), str(e))) 



    def _get_client(self, key_path, project): 
        if key_path is not None: 
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=[
                    "https://www.googleapis.com/auth/bigquery"],
            )

            client = bigquery.Client(credentials=credentials,project=credentials.project_id)
        elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None: 
            client = bigquery.Client(project=project)
        else: 
            raise Exception("Must either provide GOOGLE_KEYFILE in lolpop configuration or set environment variable GOOGLE_APPLICATION_CREDENTIALS.")

        return client
    
    def _get_format(self, extension): 
        if extension == ".csv": 
            return "text/csv"
        else: 
            return "application/octet-stream"