# SnowflakeDataConnector

`SnowflakeDataConnector` is a subclass of `BaseDataConnector` that allows retrieving and saving data to a Snowflake Data Warehouse. It provides methods for loading data from a Snowflake database to pandas DataFrame, and for saving a pandas DataFrame to a Snowflake database.

## Configuration

### Required Configuration

- `SNOWFLAKE_ACCOUNT` - The name of the Snowflake account.
- `SNOWFLAKE_USER` - The username for the Snowflake account.
- `SNOWFLAKE_PASSWORD` - The password for the Snowflake account.
- `SNOWFLAKE_DATABASE` - The name of the Snowflake database.
- `SNOWFLAKE_SCHEMA` - The name of the schema to use in Snowflake.
- `SNOWFLAKE_WAREHOUSE` - The name of the Snowflake warehouse to use.

### Optional Configuration 

There is no optional configuration. 

### Default Configuration 
There is no default configuration. 


## Methods 
### get_data 

The `get_data()` method retrieves data from the SnowflakeDataConnector by executing a query. 
```python
def get_data(self, table, sql=None, *args, **kwargs):
```

**Arguments** 

- `table` - The name of the table to retrieve data from (default: None).
- `sql` - The SQL command to execute (default: None) if table argument is not provided.

**Returns**
The method returns a pandas DataFrame containing the data retrieved from the Snowflake data warehouse.

**Example Usage:**

```python
from lolpop.component import SnowflakeDataConnector

config = {
    #insert component configuration here 
}

snowflake_conn = SnowflakeDataConnector(conf=config)
data = snowflake_conn.get_data('my_table')
```

### save_data 

The `save_data()` method saves a pandas DataFrame to a Snowflake data warehouse. It checks if the table already exists, and modifies its definition if it needs to.

```python
def save_data(self, data, table, *args, **kwargs):
```

 **Arguments**:

- `data` - The pandas DataFrame to save.
- `table` - The name of the table to save the data to.

**Example Usage:**

```python
from lolpop.component import SnowflakeDataConnector

config = {
    #insert component configuration here 
}

snowflake_conn = SnowflakeDataConnector(conf=config)

data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
snowflake_conn.save_data(data, 'my_table')
```

### _load_data 
The `_load_data` method loads data from the Snowflake data warehouse and returns it as a pandas DataFrame.

```python
def _load_data(self, sql, config, *args, **kwargs):
```
 **Arguments**:

- `data` (pandas.DataFrame) - The pandas DataFrame to save.
- `table` (str) - The name of the table to save the data to.
- `config` (dict) - Snowflake configuration

**Returns**
The method returns a pandas DataFrame containing the data retrieved from the Snowflake data warehouse.

### save_ data 
The `_save_data()` method saves a pandas DataFrame to the Snowflake data warehouse. 

```python
def _save_data(self, data, table_name, config, *args, **kwargs):
```

**Arguments**:

- `data` - The pandas DataFrame to save
- `table_name` - The name of the table to save the data to.
- `config` - The configuration for the Snowflake data warehouse.


### __map_pandas_col_type_to_sf_type

The `__map_pandas_col_type_to_sf_type` method maps a pandas DataFrame column type to the corresponding Snowflake data type.

```python
def __map_pandas_col_type_to_sf_type(self, col_type):
```

**Arguments** 

- `col_type` The data type of the pandas DataFrame column. 

**Returns**: 
Returns the corresponding Snowflake data type as a string.

## Example Usage

```python
from lolpop.component import SnowflakeDataConnector
import pandas as pd

config = {
    #insert component config here
}

# Initialize an instance of the class
snowflake_conn = SnowflakeDataConnector(conf=config)

# Retrieve data from a table
df = snowflake_conn.get_data('table_name')

# Save data to a table
data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
snowflake_conn.save_data(data, 'table_name')
```