# DatabricksSQLDataConnector

This class provides functionality for interfacing with a Databricks SQL data connector in Python. The class has methods for retrieving data from the specified SQL table or a provided SQL query, and for saving given data to a specific table in Databricks SQL or updating the existing table's structure as necessary. The class extends the `BaseDataConnector` class.

## Configuration

### Required Configuration

- `DATABRICKS_SERVER_HOSTNAME`: The Databricks sql server hostname.

- `DATABRICKS_HTTP_PATH`: The Databricks server HTTP path. 

- `DATABRICKS_TOKEN`: The Databricks token to use. 

- `DATABRICKS_CATALOG`: The Databricks catalog to read data from/save data into. 

- `DATABRICKS_SCHEMA`: The Databricks schema to read data from/save data into. 

### Optional Configuration 
There is no optional configuration.

### Default Configuration 
There is no default configuration. 

## Methods

### get_data

Returns data from the given Databricks SQL table or from a provided SQL query in DataFrame format.

```python
get_data(self, table, sql=None, *args, **kwargs)
```

**Arguments:**
- `table`: Name of the SQL table to retrieve data from.
- `sql`: SQL Query to retrieve data from Databricks SQL table.

**Returns:**
- `pd.DataFrame`: DataFrame containing the data from either the Databricks SQL table or from the SQL query passed.


### save_data

Saves data to a specific table in Databricks or updates the existing table's structure as necessary.

```python
save_data(self, data, table, *args, **kwargs)
```

**Arguments:**
- `data`: DataFrame containing the data to be saved to a Databricks SQL table.
- `table`: Name of the SQL table to save data to.

**Returns:**
- None

### _load_data 

This method executes the given SQL command in Databricks SQL and returns the retrieved data. 

```python 
_load_data(self, sql, config, *args, **kwargs)
```
**Arguments**:

- `sql`: (str) SQL command to execute.
- `config`: (dict) Configuration information for Databricks.

**Returns**

- `pandas.DataFrame`: Fetched data from Databricks SQL.

### _save_data

```python 
_save_data(self, data, table_name, config, *args, **kwargs)
```

This method saves the given data to a table in Databricks SQL. 

 **Arguments**:

- `data`: (pandas.DataFrame) The data to save
- `table_name`: (str) Name of table to save data
- `config`: (dict) Configuration file for Databricks.

### __map_pandas_col_type_to_databrickssql_type

Maps the given pandas column data type to a Databricks SQL data type.

```python
_def __map_pandas_col_type_to_databrickssql_type(self, col_type)
```

**Arguments**:

- `col_type`: pandas column type

**Returns**:

- `str`: Databricks column type.


## Usage

```python
from lolpop.component import DatabricksSQLDataConnector 

config = {
    #insert component config
}

# Create an instance of `DatabricksSQLDataConnector`
connector = DatabricksSQLDataConnector(conf=config)

# Retrieve data from the "employee" table
data = connector.get_data("employee")

#save data to a new table
connector.save_data(data, "new_table")
```