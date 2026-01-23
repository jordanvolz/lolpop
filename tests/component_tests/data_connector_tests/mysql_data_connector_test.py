import pytest
from unittest.mock import patch, Mock
import pandas as pd
from pandas.testing import assert_frame_equal

from lolpop.component.data_connector.mysql_data_connector import MySQLDataConnector


class TestMySQLDataConnector:
    """Test class for all the methods in MySQLDataConnector"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mysql_data_connector = MySQLDataConnector(
            conf={"config": {
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": 3306,
                "MYSQL_USER": "user",
                "MYSQL_PASSWORD": "password",
                "MYSQL_DBNAME": "db",
            }},
            skip_config_validation=True,
            dependent_integrations={"component": {"metadata_tracker": Mock()}},
            is_standalone=True,
        )

    @patch("lolpop.component.data_connector.mysql_data_connector.pymysql.connect")
    def test__get_connector(self, mock_connect):
        mock_connect.return_value = True

        assert MySQLDataConnector._get_connector({
            "MYSQL_HOST": "localhost",
            "MYSQL_PORT": 3306,
            "MYSQL_USER": "user",
            "MYSQL_PASSWORD": "password",
            "MYSQL_DBNAME": "db",
        })
        mock_connect.assert_called_once()

    def test__map_pandas_col_type_to_mysql_type(self):
        assert self.mysql_data_connector._MySQLDataConnector__map_pandas_col_type_to_mysql_type(
            pd.Series(pd.date_range("2024-01-01", periods=1)).dtype
        ) == "DATETIME"
        assert self.mysql_data_connector._MySQLDataConnector__map_pandas_col_type_to_mysql_type(
            pd.Series(pd.to_timedelta([1], unit="D")).dtype
        ) == "BIGINT"
        assert self.mysql_data_connector._MySQLDataConnector__map_pandas_col_type_to_mysql_type(pd.DataFrame({"test": [True]}).test.dtype) == "BOOLEAN"
        assert self.mysql_data_connector._MySQLDataConnector__map_pandas_col_type_to_mysql_type(pd.DataFrame({"test": [1]}).test.dtype) == "BIGINT"
        assert self.mysql_data_connector._MySQLDataConnector__map_pandas_col_type_to_mysql_type(pd.DataFrame({"test": [1.0]}).test.dtype) == "DOUBLE"
        assert self.mysql_data_connector._MySQLDataConnector__map_pandas_col_type_to_mysql_type(pd.DataFrame({"test": ["test"]}).test.dtype) == "TEXT"

    @patch.object(MySQLDataConnector, "_get_connector")
    def test__load_data(self, mock_get_connector):
        class DummyCursor:
            description = [("col1",), ("col2",)]

            def execute(self, sql):
                self.sql = sql

            def __iter__(self):
                return iter([(1, "a"), (2, "b")])

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        class DummyConnection:
            def cursor(self):
                return DummyCursor()

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        mock_get_connector.return_value = DummyConnection()

        expected = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        result = self.mysql_data_connector._load_data(
            "SELECT * FROM test",
            self.mysql_data_connector.mysql_config,
        )
        assert_frame_equal(result, expected)

    @patch.object(MySQLDataConnector, "_load_data")
    def test_get_data(self, mock_load_data):
        data = pd.DataFrame({"test": [1]})
        mock_load_data.return_value = data

        assert_frame_equal(self.mysql_data_connector.get_data("table_test"), data)
        mock_load_data.assert_called_once_with("SELECT * FROM table_test", self.mysql_data_connector.mysql_config)

        assert_frame_equal(self.mysql_data_connector.get_data(None, "SELECT * FROM table_test"), data)
        mock_load_data.assert_called_with("SELECT * FROM table_test", self.mysql_data_connector.mysql_config)

        with pytest.raises(Exception):
            self.mysql_data_connector.get_data(None, None)

    @patch.object(MySQLDataConnector, "_save_data")
    def test_save_data_new_table(self, mock_save_data):
        data = pd.DataFrame({"test": [1]})
        mock_tables = pd.DataFrame({"table_name": ["other_table"]})
        self.mysql_data_connector.get_data = Mock(return_value=mock_tables)

        self.mysql_data_connector.save_data(data, "table_test")
        mock_save_data.assert_called_once_with(data, "table_test", self.mysql_data_connector.mysql_config)

    @patch.object(MySQLDataConnector, "_save_data")
    @patch.object(MySQLDataConnector, "_MySQLDataConnector__map_pandas_col_type_to_mysql_type")
    def test_save_data_existing_table_with_new_and_deleted_cols(self, mock_map_col, mock_save_data):
        mock_tables = pd.DataFrame({"table_name": ["table_test"]})
        schema_table = pd.DataFrame({"existing_col": ["TEXT"]})
        self.mysql_data_connector.get_data = Mock(side_effect=[mock_tables, schema_table, pd.DataFrame()])
        mock_map_col.return_value = "TEXT"

        new_data = pd.DataFrame({"new_col": [1]})
        self.mysql_data_connector.save_data(new_data, "table_test")

        expected = pd.DataFrame({"new_col": [1], "existing_col": [None]})
        args, kwargs = mock_save_data.call_args
        assert args[1] == "table_test"
        assert args[2] == self.mysql_data_connector.mysql_config
        assert_frame_equal(args[0], expected)
