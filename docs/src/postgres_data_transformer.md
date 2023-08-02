# PostgresDataTransformer

The `PostgresDataTransformer` class is a Python class that inherits from the `BaseDataTransformer` class. This class provides methods to retrieve data from a Postgres database using the PostgreSQL Python adapter (psycopg2) and transform it into a pandas dataframe.

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

### transform
This method is used to retrieve data from a PostgreSQL database by passing a SQL query to the `PostgresDataConnector._load_data` method. This method returns a pandas dataframe containing the retrieved data.

```python 
transform(sql, *args, **kwargs)
```


**Arguments**: 

* `sql` (str): A string containing the SQL query to be executed

**Returns**:

* `data` (pandas dataframe): A pandas dataframe containing the data retrieved from the PostgreSQL database

## Usage

```python
from lolpop.component import PostgresDataTransformer


config = {
    #insert component config
}

# Define a SQL query to retrieve data from the PostgreSQL database
sql_query = "SELECT * FROM my_table;"

# Create an instance of the PostgresDataTransformer class
pg_transformer = PostgresDataTransformer(conf=config)

# Call the transform method to retrieve the data from the PostgreSQL database
data = pg_transformer.transform(sql_query)

# Print the retrieved data
print(data.head())
```