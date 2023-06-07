import pytest
from unittest.mock import patch, Mock
from pandas.util.testing import assert_frame_equal
from google.cloud import bigquery
from google.oauth2 import service_account
from data_connector import BigQueryDataConnector
import pandas as pd
import os


class TestBigQueryDataConnector:
    """Test class for all the methods in BigQueryDataConnector"""

    @pytest.fixture
    def setup(self):
        self.bigquery_data_connector = BigQueryDataConnector(
            config={"GOOGLE_PROJECT": "project-test"})

    @patch("data_connector.bigquery.Client")
    def test__get_client(self, mock_client):
        mock_client.return_value = True
        
        assert self.bigquery_data_connector._get_client("path/to/keyfile", "project-test")

        # testing if missing GOOGLE_APPLICATION_CREDENTIALS raise an exception 
        with pytest.raises(Exception):
            self.bigquery_data_connector._get_client(None, "project-test")


    def test__map_pandas_col_type_to_bg_type(self):
        assert self.bigquery_data_connector._map_pandas_col_type_to_bg_type(pd.Timestamp) == "DATETIME"
        assert self.bigquery_data_connector._map_pandas_col_type_to_bg_type(pd.Timedelta) == "INTERVAL"
        assert self.bigquery_data_connector._map_pandas_col_type_to_bg_type(pd.DataFrame({"test" : [True]}).test.dtype) == "BOOL"
        assert self.bigquery_data_connector._map_pandas_col_type_to_bg_type(pd.DataFrame({"test" : [1]}).test.dtype) == "INT64"
        assert self.bigquery_data_connector._map_pandas_col_type_to_bg_type(pd.DataFrame({"test" : [1.0]}).test.dtype) == "FLOAT64"
        assert self.bigquery_data_connector._map_pandas_col_type_to_bg_type(pd.DataFrame({"test" : ["test"]}).test.dtype) == "STRING"        

    
    def test__get_format(self):
        assert self.bigquery_data_connector._get_format(".csv") == "text/csv"
        assert self.bigquery_data_connector._get_format(".pdf") == "application/octet-stream"


    @patch("data_connector.bigquery.Client")
    def test__save_data(self, mock_client):
        # testing successful upload
        mock_client.return_value.load_table_from_dataframe.return_value.result.return_value = True
        with patch.object(self.bigquery_data_connector, "log") as mock_log:
            self.bigquery_data_connector._save_data(pd.DataFrame(), "table_test", {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"})
            mock_log.assert_called_once_with("Successfully uploaded table table_test to dataset dataset-test")

        # testing unsuccessful upload
        mock_client.return_value.load_table_from_dataframe.side_effect = Exception('failed to create job pack to bigquery')
        with patch.object(self.bigquery_data_connector, "log") as mock_log:
            self.bigquery_data_connector._save_data(pd.DataFrame(), "table_test", {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"})
            mock_log.assert_called_once_with("Failed to upload table table_test to dataset dataset-test: failed to create job pack to bigquery")
            

    @patch.object(BigQueryDataConnector, "_get_client")
    def test__load_data(self, mock_get_client):
        mock_client = Mock(spec=bigquery.Client)
        mock_get_client.return_value = mock_client

        data = pd.DataFrame({"test" : [1]})
        table = "test_table"
        sql = "SELECT * FROM test_table"
        mock_client.query.return_value.to_dataframe.return_value = data
        
        assert_frame_equal(data, self.bigquery_data_connector._load_data(sql, {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"}))
            

    @patch.object(BigQueryDataConnector, "_load_data")
    def test_get_data(self, mock_load_data):
        data = pd.DataFrame({"test" : [1]})
        mock_load_data.return_value = data

        # Testing table param
        assert_frame_equal(self.bigquery_data_connector.get_data("table_test"), data)
        mock_load_data.assert_called_once_with("SELECT * FROM table_test", {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"})

        # Testing sql param
        assert_frame_equal(self.bigquery_data_connector.get_data(None, "SELECT * FROM table_test"), data)
        mock_load_data.assert_called_with("SELECT * FROM table_test", {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"})        

        # Testing exception due to missing params
        with pytest.raises(Exception):
            self.bigquery_data_connector.get_data(None, None)


    @patch.object(BigQueryDataConnector, "_get_client")
    @patch.object(BigQueryDataConnector, "_load_data")
    def test_save_data(self, mock_load_data, mock_get_client):
        data = pd.DataFrame({"test" : [1]})
        mock_load_data.return_value = data

        # Testing save in existing table
        mock_tables = pd.DataFrame({"table_name" : ["table_test"]})
        self.bigquery_data_connector.get_data = Mock(return_value=mock_tables)
        with patch.object(self.bigquery_data_connector, "_save_data") as mock_save_data:
            self.bigquery_data_connector.save_data(data, "table_test")
            mock_save_data.assert_called_once_with(data, "table_test", {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"})        

        # Testing add column in existing table
        mock_tables = pd.DataFrame({"table_name" : ["table_test"]})
        schema_table = pd.DataFrame({"test" : ["INT64"]})
        self.bigquery_data_connector.get_data = Mock(side_effect=[mock_tables, schema_table])
        with patch.object(self.bigquery_data_connector, "_save_data") as mock_save_data, patch.object(self.bigquery_data_connector, "_map_pandas_col_type_to_bg_type") as mock_map_col:
            mock_map_col.return_value = "INT64"
            self.bigquery_data_connector.save_data(pd.DataFrame({"new_col" : [1]}), "table_test")
            mock_save_data.assert_called_once_with(pd.DataFrame({"new_col" : [1], "test" : [None]}), "table_test", {"GOOGLE_KEYFILE": "test", "GOOGLE_PROJECT": "project-test", "GOOGLE_DATASET": "dataset-test"})          
            
        # Testing missing GOOGLE_DATASET
        with pytest.raises(Exception):
            self.bigquery_data_connector.save_data(data, "table_test", GOOGlE_DATASET=None)