# RedshiftDataTransformer Class Documentation


## Description

The `RedshiftDataTransformer` class provides a set of methods for retrieving data from Amazon Redshift databases. It provides a `transform` method that retrieves data from a RedshiftDataConnector object based on the SQL query provided.


## Constructor

### `__init__(self, *args, **kwargs)`

The constructor initializes a RedshiftDataTransformer object. It loads the required configuration details from the given configuration file passed as an argument. It also initializes `self.redshift_config` and `self.pg_config` attributes.

- `args`: variable arguments passed to the constructor
- `kwargs`: keyword arguments passed to the constructor


## Methods

### `transform(self, sql, *args, **kwargs)`

The `transform` method retrieves data based on the SQL query provided.

- `sql`: SQL query to retrieve data from the database
- `args`: positional arguments passed to the method
- `kwargs`: keyword arguments passed to the method
- Returns:
  * `data` (pandas dataframe): A pandas dataframe containing the data retrieved from the Redshift database


## Examples

```python
import RedshiftDataTransformer

# Initialize RedshiftDataTransformer object
redshift_transformer = RedshiftDataTransformer()

# Set required SQL query
query = 'SELECT * FROM my_table'

# Retrieve data based on the SQL query
data = redshift_transformer.transform(query)

# Print the retrieved data
print(data)
```

Output:
```
  column1  column2  column3
0   value1   value2   value3
1   value4   value5   value6
```