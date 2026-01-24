# MySQLDataConnector

The `MySQLDataConnector` is a Python class that is used to connect to a MySQL database and retrieve and store data. This class inherits from the `BaseDataConnector` class and overrides some of its methods to be customized for MySQL databases. The class also includes some additional methods that are specific to MySQL.

## Configuration

### Required Configuration

- `MYSQL_HOST`: Hostname of the MySQL db.
- `MYSQL_PORT`: Port used by the MySQL db.
- `MYSQL_USER`: User to use to connect to the MySQL db.
- `MYSQL_PASSWORD`: Password for `MYSQL_USER`.
- `MYSQL_DBNAME`: MySQL database to use to load/save data.

### Optional Configuration

There is no optional configuration.

### Default Configuration

There is no default configuration.

## Methods

### get_data

This method retrieves data from the MySQL database.

```python
get_data(self, table, sql=None, *args, **kwargs)
```

**Arguments**:

- `table` (str): The name of the table to retrieve data from.
- `sql` (str): A SQL query string that can be used to retrieve data from the database. If no `sql` argument is provided and `table` is not `None`, the method constructs a SQL query to retrieve all columns from the specified table.

**Returns**:

- `pandas.DataFrame`: Dataframe containing the retrieved data.

### save_data

This method saves data to a table in the MySQL database.

```python
save_data(self, data, table, *args, **kwargs)
```

**Arguments**:

- `data` (pandas.Dataframe): DataFrame that contains the data to be saved to the database table.
- `table` (str): The name of the table in the database that the data should be saved to.

### _load_data

This method is a helper method that is used internally by the `get_data` method to load data from the MySQL database into a Pandas DataFrame.

```python
_load_data(self, sql, config)
```

**Arguments**:

- `sql` (str): A SQL query string that is used to retrieve data from the database.
- `config` (dict): Contains the configuration parameters for the database connection.

**Returns**:

- `pandas.DataFrame`: DataFrame containing the retrieved data.

### _save_data

This method is a helper method that is used internally by the `save_data` method to save data to a table in the MySQL database.

```python
_save_data(self, data, table, config)
```

**Arguments**:

- `data` (pandas.DataFrame): DataFrame that contains the data to be saved to the database table.
- `table` (str): The name of the table in the database that the data should be saved to.
- `config` (dict): Contains the configuration parameters for the database connection.

### __map_pandas_col_type_to_mysql_type

This method is a helper method that maps Pandas data types to MySQL data types.

```python
__map_pandas_col_type_to_mysql_type(self, col_type)
```

**Arguments**:

- `col_type`: Pandas data type that needs to be mapped.

**Returns**:

- `str`: The MySQL data type that corresponds to the Pandas data type.

### _get_connector

This method is a helper method that gets a connection object to the MySQL database using the configuration parameters specified in the `config` dictionary.

```python
_get_connector(config)
```

**Arguments**:

- `config` (dict): Configuration for MySQL database.

**Returns**:

- `connection` object representing the connection to the MySQL db.

## Usage

```python
from lolpop.component import MySQLDataConnector
import pandas as pd


config = {
    #insert component config here
}

# Instantiate a MySQLDataConnector object
mysqldc = MySQLDataConnector(conf=config)

# Retrieve data from a table in the database
df = mysqldc.get_data("my_table")

# Save data to a table in the database
new_data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
mysqldc.save_data(new_data, "my_table2")
```

### Quick Local Smoke Test (SQLAlchemy)

```python
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:rootpw@127.0.0.1:3306/lolpop_test")

# 1) create a small dataset in memory
df = pd.DataFrame({"id": [1, 2], "name": ["alice", "bob"]})

# 2) write it to MySQL
df.to_sql("people", engine, if_exists="replace", index=False)

# 3) read it back from MySQL
loaded = pd.read_sql(text("SELECT * FROM people"), engine)

# 4) print it
print(loaded)
```
