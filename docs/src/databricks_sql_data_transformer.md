# DatabricksSQLDataTransformer

The `DatabricksSQLDataTransformer` class is a subclass of `BaseDataTransformer`. This class provides a way to transform data from a Databricks SQL data source.

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


### transform 

This method is used to transform data from a Databricks SQL data source. It takes a SQL statement for querying the Databricks data source as input and returns a Pandas DataFrame of transformed data.

```python
transform(sql, *args, **kwargs)
```


**Arguments**: 

- `sql`: (str) A SQL statement for querying the Databricks data source.


**Returns**: 

`data` (pandas.DataFrame): A DataFrame of transformed data.

##  Usage

```python
from lolpop.component import DatabricksSQLDataTransformer

config = {
    #insert component config here
}

data_transformer = DatabricksSQLDataTransformer(conf=config)
sql_statement = "SELECT * FROM my_table"
transformed_data = data_transformer.transform(sql_statement)
``` 
