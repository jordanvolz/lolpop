# Class: PostgresDataConnector

The `PostgresDataConnector` is a Python class that is used to connect to a Postgres database and retrieve and store data. This class inherits from the `BaseDataConnector` class and overrides some of its methods to be customized for Postgres databases. The class also includes some additional methods that are specific to Postgres. The `PostgresDataConnector` class is defined as follows:

```python
@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class PostgresDataConnector(BaseDataConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pg_config = utils.load_config(["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DBNAME", "POSTGRES_SCHEMA"], self.config)

    def get_data(self, table, sql=None, *args, **kwargs):
        """
        Retrieves data from the database.

        Args:
            table (str): name of database table to retrieve data from
            sql (str): SQL query to retrieve data, defaults to None

        Returns:
            pandas.DataFrame: retrieved data
        """

    def save_data(self, data, table, *args, **kwargs):
        """
        Saves data to a database table.

        Args:
            data (pandas.DataFrame): data to save to the database
            table (str): name of database table to save data to
        """

    @classmethod
    def _load_data(self, sql, config):
        """
        Loads data into a pandas DataFrame object.

        Args:
            sql (str): SQL query to retrieve data
            config (dict): configuration dictionary

        Returns:
            pandas.DataFrame: data from database

        """

    def _save_data(self, data, table, config):
        """
        Saves data to a database table.

        Args:
            data (pandas.DataFrame): data to save to the database
            table (str): name of database table to save data to
            config (dict): configuration dictionary

        """

    def _map_pandas_col_type_to_duckdb_type(self, col_type):
        """_summary_

        Maps column data types from pandas to Postgres.

        Args:
            col_type (pd.dtype): pandas data type

        Returns:
            str: corresponding data type for Postgres
        """
    
    def _get_connector(config):
```

## Methods

### `__init__(self, *args, **kwargs)`

The class constructor method, `__init__`, initializes the `PostgresDataConnector` class object. It calls the constructor method of the `BaseDataConnector` class to instantiate the object, and then sets the configuration parameters for the Postgres database connection. The configuration parameters are loaded using the `load_config` method of the `utils` module.

### `get_data(self, table, sql=None, *args, **kwargs)`

This method retrieves data from the Postgres database. The `table` argument is a string that specifies the name of the table to retrieve data from. The optional `sql` argument is a SQL query string that can be used to retrieve data from the database. If no `sql` argument is provided and `table` is not `None`, the method constructs a SQL query to retrieve all columns from the specified table. The method returns a Pandas DataFrame containing the retrieved data.

### `save_data(self, data, table, *args, **kwargs)`

This method saves data to a table in the Postgres database. The `data` argument is a Pandas DataFrame that contains the data to be saved to the database table. The `table` argument is a string that specifies the name of the table in the database that the data should be saved to. If the specified table already exists in the database, the method checks if any columns have been added or deleted from the DataFrame and updates the table schema accordingly. Once the table schema is updated, or if the table does not already exist, the method saves the data to the table.

### `_load_data(self, sql, config)`

This method is a helper method that is used internally by the `get_data` method to load data from the Postgres database into a Pandas DataFrame. The `sql` argument is a SQL query string that is used to retrieve data from the database. The `config` argument is a dictionary that contains the configuration parameters for the database connection. The method returns a Pandas DataFrame containing the retrieved data.

### `_save_data(self, data, table, config)`

This method is a helper method that is used internally by the `save_data` method to save data to a table in the Postgres database. The `data` argument is a Pandas DataFrame that contains the data to be saved to the database table. The `table` argument is a string that specifies the name of the table in the database that the data should be saved to. The `config` argument is a dictionary that contains the configuration parameters for the database connection.

### `_map_pandas_col_type_to_duckdb_type(self, col_type)`

This method is a helper method that maps Pandas data types to Postgres data types. The `col_type` argument is a Pandas data type that needs to be mapped. The method returns a string that represents the Postgres data type that corresponds to the Pandas data type.

### `_get_connector(config)`

This method is a helper method that gets a connection object to the Postgres database using the configuration parameters specified in the `config` dictionary.


## Usage

```python
from PostgresDataConnector import PostgresDataConnector
import pandas as pd

# Instantiate a PostgresDataConnector object
pgdc = PostgresDataConnector(config)

# Retrieve data from a table in the database
df = pgdc.get_data("my_table")

# Save data to a table in the database
new_data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
pgdc.save_data(new_data, "my_table2")

```