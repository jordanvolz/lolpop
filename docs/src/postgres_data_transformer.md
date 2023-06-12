# Class: PostgresDataTransformer

The `PostgresDataTransformer` class is a Python class that inherits from the `BaseDataTransformer` class. This class provides methods to retrieve data from a Postgres database using the PostgreSQL Python adapter (psycopg2) and transform it into a pandas dataframe.

## Required Configurations

The `PostgresDataTransformer` class requires the following configurations to be provided in its `config` attribute:
* `POSTGRES_HOST`: the host name or IP address of the PostgreSQL database server
* `POSTGRES_PORT`: the port number on which the PostgreSQL server is listening
* `POSTGRES_USER`: the username to connect to the PostgreSQL database
* `POSTGRES_PASSWORD`: the password to authenticate the user
* `POSTGRES_DBNAME`: the name of the database to connect to
* `POSTGRES_SCHEMA`: the schema name from which to retrieve the data

## Methods

### 1. `__init__(*args, **kwargs)`

This method is the constructor of the `PostgresDataTransformer` class. It initializes the `pg_config` attribute which is a dictionary of PostgreSQL configurations required to establish a connection and retrieve data from the database. The `load_config` method from the `utils` module is used to retrieve the PostgreSQL configurations from the `config` attribute.

### 2. `transform(sql, *args, **kwargs)`

This method is used to retrieve data from a PostgreSQL database by passing a SQL query to the `PostgresDataConnector._load_data` method. This method returns a pandas dataframe containing the retrieved data.

#### Parameters
* `sql` (str): A string containing the SQL query to be executed

#### Returns
* `data` (pandas dataframe): A pandas dataframe containing the data retrieved from the PostgreSQL database

### Example Usage

```python
# Import the necessary classes and modules
import pandas as pd
from myapp.utils import (
    load_config,
    error_handler,
    log_execution,
)
from myapp.data_connectors.postgres_data_connector import PostgresDataConnector
from myapp.data_transformers.base_data_transformer import BaseDataTransformer
from myapp.data_transformers.postgres_data_transformer import PostgresDataTransformer

# Define a SQL query to retrieve data from the PostgreSQL database
sql_query = "SELECT * FROM my_table;"

# Create an instance of the PostgresDataTransformer class
pg_transformer = PostgresDataTransformer(config=load_config("my_config.ini"))

# Call the transform method to retrieve the data from the PostgreSQL database
data = pg_transformer.transform(sql_query)

# Print the retrieved data
print(data.head())
```