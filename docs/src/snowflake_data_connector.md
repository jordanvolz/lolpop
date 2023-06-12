# SnowflakeDataConnector Class

`SnowflakeDataConnector` is a subclass of `BaseDataConnector` that allows retrieving and saving data to a Snowflake Data Warehouse. It provides methods for loading data from a Snowflake database to pandas DataFrame, and for saving a pandas DataFrame to a Snowflake database.

## Class Declaration

```python
@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class SnowflakeDataConnector(BaseDataConnector):
```

The class declaration defines a decorator for all methods in the class. `@utils.error_handler` and `@utils.log_execution()` are decorators provided by the parent class. The class also inherits from `BaseDataConnector`.

## Class Attributes

```python
__REQUIRED_CONF__ = {"config": ["SNOWFLAKE_ACCOUNT",
                                "SNOWFLAKE_USER",
                                "SNOWFLAKE_PASSWORD",
                                "SNOWFLAKE_DATABASE",
                                "SNOWFLAKE_SCHEMA",
                                "SNOWFLAKE_WAREHOUSE"]}
```

The `__REQUIRED_CONF__` attribute is a dictionary that stores the configuration options required to create an instance of `SnowflakeDataConnector`. It requires the following parameters:

- `SNOWFLAKE_ACCOUNT` - The name of the Snowflake account.
- `SNOWFLAKE_USER` - The username for the Snowflake account.
- `SNOWFLAKE_PASSWORD` - The password for the Snowflake account.
- `SNOWFLAKE_DATABASE` - The name of the Snowflake database.
- `SNOWFLAKE_SCHEMA` - The name of the schema to use in Snowflake.
- `SNOWFLAKE_WAREHOUSE` - The name of the Snowflake warehouse to use.

## Class Methods

### `__init__(self, *args, **kwargs)`

```python
def __init__(self, *args, **kwargs):
```

The constructor method for the `SnowflakeDataConnector` class. It initializes an instance of the class with the necessary configuration. It uses the `utils.load_config()` method to load in the configuration options for Snowflake. It inherits the initialization from the parent class `BaseDataConnector`.

### `get_data(self, table, sql=None, *args, **kwargs)`

```python
def get_data(self, table, sql=None, *args, **kwargs):
```

The `get_data()` method retrieves data from the SnowflakeDataConnector by executing a query. It takes the following parameters:

- `table` - The name of the table to retrieve data from (default: None).
- `sql` - The SQL command to execute (default: None) if table argument is not provided.

The method returns a pandas DataFrame containing the data retrieved from the Snowflake data warehouse.

**Example Usage:**

```python
snowflake_conn = SnowflakeDataConnector(...)
data = snowflake_conn.get_data('my_table')
```

### `save_data(self, data, table, *args, **kwargs)`

```python
def save_data(self, data, table, *args, **kwargs):
```

The `save_data()` method saves a pandas DataFrame to a Snowflake data warehouse. It checks if the table already exists, and modifies its definition if it needs to. It takes the following parameters:

- `data` - The pandas DataFrame to save.
- `table` - The name of the table to save the data to.

**Example Usage:**

```python
snowflake_conn = SnowflakeDataConnector(...)
data = load_data_from_source()
snowflake_conn.save_data(data, 'my_table')
```

### `_map_pandas_col_type_to_sf_type(self, col_type)`

```python
def _map_pandas_col_type_to_sf_type(self, col_type):
```

The '_map_pandas_col_type_to_sf_type` method maps a pandas DataFrame column type to the corresponding Snowflake data type. It takes the `col_type` parameter, which is the data type of the pandas DataFrame column. It returns the corresponding Snowflake data type as a string.

### `_load_data(self, sql, config)`

```python
@classmethod
def _load_data(self, sql, config):
```

The `_load_data` method loads data from the Snowflake data warehouse and returns it as a pandas DataFrame. It executes the SQL statement using the `get_from_snowflake()` method. It returns the retrieved data as a pandas DataFrame.

### `_save_data(self, data, table_name, config)`

```python
def _save_data(self, data, table_name, config):
```

The `_save_data()` method saves a pandas DataFrame to the Snowflake data warehouse. It uses the `save_to_snowflake()` method to execute an "INSERT INTO" statement to save the data to the specified table. It takes the following parameters:

- `data` - The pandas DataFrame to save
- `table_name` - The name of the table to save the data to.
- `config` - The configuration for the Snowflake data warehouse.

## Example Usage

```python
from data_connectors.snowflake_connector import SnowflakeDataConnector
import pandas as pd

# Initialize an instance of the class
snowflake_conn = SnowflakeDataConnector()

# Retrieve data from a table
df = snowflake_conn.get_data('table_name')

# Save data to a table
data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
snowflake_conn.save_data(data, 'table_name')
```