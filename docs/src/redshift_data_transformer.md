# RedshiftDataTransformer


The `RedshiftDataTransformer` class provides a set of methods for retrieving data from Amazon Redshift databases. It provides a `transform` method that retrieves data from a RedshiftDataConnector object based on the SQL query provided.

## Configuration 

### Required Configuration

- `REDSHIFT_HOST`: Hostname of the Redshift db.
- `REDSHIFT_PORT`: Port used by the Redshift db.
- `REDSHIFT_USER`: User to use to connect to the Redshift db.
- `REDSHIFT_PASSWORD`: Password for `REDSHIFT_USER`.
- `REDSHIFT_DBNAME`: Redshift database to use to load/save data. 
- `REDSHIFT_SCHEMA`: Default Redshift schema to use. 

### Optional Configuration 

There is no optional configuration. 

### Default Configuration 
There is no default configuration. 

## Methods

### transform 
The `transform` method retrieves data based on the SQL query provided.


```python 
transform(self, sql, *args, **kwargs)
```

**Arguments**: 

- `sql`: SQL query to retrieve data from the database

**Returns**:

  * `data` (pandas dataframe): A pandas dataframe containing the data retrieved from the Redshift database


## Usage

```python
from lolpop.component import RedshiftDataTransformer

config = {
  #insert component config here 
}

# Initialize RedshiftDataTransformer object
redshift_transformer = RedshiftDataTransformer(conf=config)

# Set required SQL query
query = 'SELECT * FROM my_table'

# Retrieve data based on the SQL query
data = redshift_transformer.transform(query)

# Print the retrieved data
print(data)
```