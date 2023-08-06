# DuckDBDataTransformer

The `DuckDBDataTransformer*`class is a Python class that inherits from the `BaseDataTransformer` class. The class provides a method to transform data by executing a given SQL query using the `DuckDBDataConnector` utility to connect to a DuckDB database.


## Configuration

### Required Configuration

- `duckdb_path`: The filepath to the duckdb instance.  

### Optional Configuration 
There is no optional configuration.

### Default Configuration 
There is no default configuration. 

## Methods



### transform 

This method transforms data using DuckDBDataConnector. 

```python
def transform(self, sql, *args, **kwargs)
```


**Arguments**: 

* `sql`: *(str)* The SQL query to transform the data.

**Returns**: 

* `data`: (pandas.DataFrame) The transformed data as a Pandas DataFrame.


## Usage


```python 
rom lolpop.component import DuckDBDataTransformer

config = {
   #insert component config here
}

transformer = DuckDBDataTransformer(conf=copnfig)
sql_query = "SELECT * FROM sample_table LIMIT 10"

result = transformer.transform(sql_query)

print(result.head())
```
