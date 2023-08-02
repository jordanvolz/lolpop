# SnowflakeDataTransformer 

The `SnowflakeDataTransformer` class is a Python class used for transforming data from a Snowflake database. This class inherits from the `BaseDataTransformer` class and has one method for data transformation.

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


### transform
This method takes a SQL statement as input and extracts data from the Snowflake database using that SQL. It returns the data extracted from the Snowflake database.

```python 
transform(self, sql, *args, **kwargs)
```



**Arguments**: 

* `sql` (str): The SQL statement used to extract data from the Snowflake database.


**Returns**: 

* `data`: The data extracted from the Snowflake database.

#### Usage

```python
from lolpop.component import SnowflakeDataTransformer 

config = {
    #insert component config here 
}

transformer = SnowflakeDataTransformer(conf=config)

data = transformer.transform("SELECT * FROM table_name")
print(data.head())
```
