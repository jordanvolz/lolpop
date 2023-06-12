# DatabricksSQLDataTransformer

The `DatabricksSQLDataTransformer` class is a subclass of `BaseDataTransformer`. This class provides a way to transform data from a Databricks SQL data source.

## Methods

### __init__(*args, **kwargs)

This method initializes an instance of the class. It also loads the required configurations for connecting to the Databricks SQL data source.

### transform(sql, *args, **kwargs)

This method is used to transform data from a Databricks SQL data source. It takes a SQL statement for querying the Databricks data source as input and returns a Pandas DataFrame of transformed data.

#### Arguments

1. `sql (str)`: A SQL statement for querying the Databricks data source.
2. `*args`: Variable length argument list.
3. `**kwargs`: Arbitrary keyword arguments.

#### Return Value

`data (pandas.DataFrame)`: A DataFrame of transformed data.

## Example Usage

```python
from databricks_sql_data_transformer import DatabricksSQLDataTransformer

data_transformer = DatabricksSQLDataTransformer(config=my_config)
sql_statement = "SELECT * FROM my_table"
transformed_data = data_transformer.transform(sql_statement)
``` 

In the above example, an instance of the `DatabricksSQLDataTransformer` class is created using configurations provided by `my_config`. Then, the `transform` method is called with a SQL statement to query the Databricks data source. Finally, the transformed data is obtained as a Pandas DataFrame and stored in the `transformed_data` variable.