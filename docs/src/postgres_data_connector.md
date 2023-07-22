# PostgresDataConnector

The `PostgresDataConnector` is a Python class that is used to connect to a Postgres database and retrieve and store data. This class inherits from the `BaseDataConnector` class and overrides some of its methods to be customized for Postgres databases. The class also includes some additional methods that are specific to Postgres. The `PostgresDataConnector` class is defined as follows:

## Configuration

### Required Configuration

- `POSTGRES_HOST`: Hostname of the Postgres db.
- `POSTGRES_PORT`: Port used by the Postgres db.
- `POSTGRES_USER`: User to use to connect to the Postgres db.
- `POSTGRES_PASSWORD`: Password for `POSTGRES_USER`.
- `POSTGRES_DBNAME`: Postgres database to use to load/save data. 
- `POSTGRES_SCHEMA`: Default Postgres schema to use. 

### Optional Configuration 

There is no optional configuration. 

### Default Configuration 
There is no default configuration. 

## Methods

### get_data 

This method retrieves data from the Postgres database. 

```python 
get_data(self, table, sql=None, *args, **kwargs)
```

**Arguments**:

- `table` (str): The name of the table to retrieve data from. The optional 
- `sql` (str): A SQL query string that can be used to retrieve data from the database. If no `sql` argument is provided and `table` is not `None`, the method constructs a SQL query to retrieve all columns from the specified table. 

**Returns**: 

- `pandas.DataFrame`: Dataframe containing the retrieved data.

### save_data 

This method saves data to a table in the Postgres database. 

```python
save_data(self, data, table, *args, **kwargs)
```

**Arguments**: 

- `data` (pandas.Dataframe): DataFrame that contains the data to be saved to the database table. 
- `table` (str): The name of the table in the database that the data should be saved to. If the specified table already exists in the database, the method checks if any columns have been added or deleted from the DataFrame and updates the table schema accordingly. Once the table schema is updated, or if the table does not already exist, the method saves the data to the table.

### _load_data 
This method is a helper method that is used internally by the `get_data` method to load data from the Postgres database into a Pandas DataFrame.

```python
_load_data(self, sql, config)
```

**Arguments**: 

- `sql` (str) : A SQL query string that is used to retrieve data from the database. 
- `config` (dict): Contains the configuration parameters for the database connection. 

**Returns**: 

- `pandas.DataFrame` DataFrame containing the retrieved data.

### _save_data 
This method is a helper method that is used internally by the `save_data` method to save data to a table in the Postgres database.

```python
_save_data(self, data, table, config)
```

**Arguments**: 

 - `data` (pandas.DataFrame): DataFrame that contains the data to be saved to the database table. 
 - `table` (str): The name of the table in the database that the data should be saved to. 
 - `config` (dict): Contains the configuration parameters for the database connection.

### __map_pandas_col_type_to_pg_type

This method is a helper method that maps Pandas data types to Postgres data types.

```python 
__map_pandas_col_type_to_pg_type(self, col_type)
```

**Arguments**

-`col_type`: Pandas data type that needs to be mapped. 

**Returns**: 

- `str`: The Postgres data type that corresponds to the Pandas data type.

### _get_connector 
This method is a helper method that gets a connection object to the Postgres database using the configuration parameters specified in the `config` dictionary.

```python
__get_connector(config)
```
**Arguments**: 

- `config` (dict): Configuration for Posgres database 

***Returns**: 

 - `connection` object representing the connection to the Postgres db. 

## Usage

```python
from lolpop.component import PostgresDataConnector
import pandas as pd


config = {
    #insert component config here 
}

# Instantiate a PostgresDataConnector object
pgdc = PostgresDataConnector(conf=config)

# Retrieve data from a table in the database
df = pgdc.get_data("my_table")

# Save data to a table in the database
new_data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
pgdc.save_data(new_data, "my_table2")

```