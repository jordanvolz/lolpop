# BigQueryDataTransformer

The `BigQueryDataTransformer` class is a Python class that inherits from the `BaseDataTransformer` class. It is used to transform data using a BigQueryDataConnector. The class allows developers to execute SQL queries in BigQuery and return the transformed data.


## Configuration 

### Required Configuration

- `GOOGLE_PROJECT`: The GCP project to connect to 

- `GOOGLE_DATASET`: The dataset in the GCP project to read/write to. 

### Optional Configuration 

- `GOOGLE_KEYFILE`: Location of a BigQuery credentials file to use in order to connect to BigQuery. If no keyfile is provided, the component will attempt to use the standard environment variable `GOOGLE_APPLICATION_CREDENTIALS`. 

### Default Configuration 
There is no default configuration. 

## Methods

The `BigQueryDataTransformer` class has the following methods:

### transform 

The `transform` method is used to transform data using the BigQueryDataConnector. 

```python 
def transform(self, sql, *args, **kwargs)
```

**Arguments**: 

* `sql` (str): The SQL query to be executed in BigQuery.


**Returns**: 

The method returns the transformed data returned by the `BigQueryDataConnector._load_data` method.

## Usage

``` python
from lolpop.component import BigQueryDataTransformer

config = {
    #insert component config here
}

sql = "SELECT * FROM my_dataset.my_table WHERE date >= '2022-01-01'"

transformer = BigQueryDataTransformer(config=conf)
data = transformer.transform(sql)
```
