# DuckDBDataTransformer Class

The *DuckDBDataTransformer* class is a Python class that inherits from the *BaseDataTransformer* class. The class provides a method to transform data by executing a given SQL query using the DuckDBDataConnector utility to connect to a DuckDB database.

## Methods

### __init__(self, *args, **kwargs)

This method initializes the DuckDBDataTransformer object. It calls the constructor of the parent class, *BaseDataTransformer*. The DuckDBDataTransformer object is created with a path to the DuckDB database specified in the configuration settings.


### transform(self, sql, *args, **kwargs)

This method transforms data using DuckDBDataConnector. 

#### Parameters

* **sql:** *(str)* The SQL query to transform the data.
* **args:** *(optional)* Optional positional arguments to pass to the DuckDBDataConnector's load_data method.
* **kwargs:** *(optional)* Optional keyword arguments to pass to the DuckDBDataConnector's load_data method.

#### Returns

* **data:** *(pandas.DataFrame)* The transformed data as a Pandas DataFrame.


## Examples

In the following code example, we'll create an instance of the DuckDBDataTransformer and use it to transform a sample SQL query that selects the first 10 rows from a sample database table.

```
import pandas as pd
from data_transformers.duckdb_transformer import DuckDBDataTransformer

transformer = DuckDBDataTransformer()
sql_query = "SELECT * FROM sample_table LIMIT 10"

result = transformer.transform(sql_query)

print(result.head())
```

Output:
```
   id      name    email  age
0   1     Alice  a@b.com   23
1   2       Bob  b@c.com   31
2   3   Charlie  c@d.com   42
3   4     David  d@e.com   27
4   5    Edward  e@f.com   19
``` 

In this example, we instantiate an instance of *DuckDBDataTransformer* object and pass a SQL query that selects the first 10 rows from some hypothetical *sample_table* table. Calling the *transform* method on the object transforms the data and returns it as a Pandas DataFrame. We then print the first 5 rows of the result to the console.