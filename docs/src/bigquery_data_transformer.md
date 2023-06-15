# Documentation for BigQueryDataTransformer class

The `BigQueryDataTransformer` class is a Python class that inherits from the `BaseDataTransformer` class. It is used to transform data using a BigQueryDataConnector. The class allows developers to execute SQL queries in BigQuery and return the transformed data.

## Class methods

The `BigQueryDataTransformer` class has the following methods:

### __init__(self, *args, **kwargs)

The `__init__` method is the constructor method for the `BigQueryDataTransformer` class. It calls the constructor method of the `BaseDataTransformer` class and loads the necessary configuration files. 

### transform(self, sql, *args, **kwargs)

The `transform` method is used to transform data using the BigQueryDataConnector. 

#### Parameters

* `sql` (str): The SQL query to be executed in BigQuery.

* `args` and `kwargs` are optional parameters that can be used to pass additional variables to the method.

#### Returns

The method returns the transformed data returned by the `BigQueryDataConnector._load_data` method.

## Example usage

```
import BigQueryDataTransformer

sql = "SELECT * FROM my_dataset.my_table WHERE date >= '2022-01-01'"

transformer = BigQueryDataTransformer(config={"GOOGLE_PROJECT": "my_project", "GOOGLE_DATASET": "my_dataset"})
data = transformer.transform(sql)
```

In the example above, we import the `BigQueryDataTransformer` class and then create a new instance of the class with a dictionary that specifies the Google project and dataset names. We then execute a SQL query on the specified dataset and save the returned transformed data to the `data` variable.