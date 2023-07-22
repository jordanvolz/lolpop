# BigQueryDataConnector

This class is a child of the BaseDataConnector class and can be used to connect to Google BigQuery. It provides methods to retrieve data from a table or using raw SQL commands as well as to save data to a BigQuery table.

## Configuration 

### Required Configuration

- `GOOGLE_PROJECT`: The GCP project to connect to 

- `GOOGLE_DATASET`: The dataset in the GCP project to read/write to. 

### Optional Configuration 

- `GOOGLE_KEYFILE`: Location of a BigQuery credentials file to use in order to connect to BigQuery. If no keyfile is provided, the component will attempt to use the standard environment variable `GOOGLE_APPLICATION_CREDENTIALS`. 

### Default Configuration 
There is no default configuration. 

## Methods

### get_data 

This method retrieves data from a table or raw SQL commmand executed in BigQuery. 

```python 
get_data(self, table, sql=None, *args, **kwargs)
```

**Arguments**:

- `table`: (str) Name of the table to fetch data from.
- `sql`: (str) SQL command to execute

**Returns**:

- `pandas.DataFrame`: fetched data

### save_data 

This method saves the given data to a table in BigQuery.

```python 
save_data(self, data, table, *args, **kwargs)
```

**Arguments**

- `data`: (pandas.DataFrame) Data to be saved.
- `table`: (str) Name of the table to save the data in.

### _load_data 

This method executes the given SQL command in BigQuery and returns the retrieved data. 

```python 
_load_data(self, sql, config, *args, **kwargs)
```
**Arguments**:

- `sql`: (str) SQL command to execute.
- `config`: (dict) Configuration information for BigQuery.

**Returns**

- `pandas.DataFrame`: Fetched data from BigQuery.

### _save_data

```python 
_save_data(self, data, table_name, config, *args, **kwargs)
```

This method saves the given data to a table in BigQuery. 

 **Arguments**:

- `data`: (pandas.DataFrame) The data to save
- `table_name`: (str) Name of table to save data
- `config`: (dict) Configuration file for bigqury project.

### _get_client

```python 
_get_client(self, key_path, project)
```

This method returns a BigQuery API client object.

**Arguments**:

- `key_path`: (str) Path to BigQuery credentials file.
- `project`: (str) Google cloud project ID.

**Returns**:

- `google.cloud.bigquery.client`: A client object for BigQuery.
### _get_format 

This method returns the MIME content type for the given file format extension.

```python
_get_format(self, extension)
```
**Arguments**:

- `extension`: (str) File extension.

**Returns**:

- `str`: MIME type.

### __map_pandas_col_type_to_bq_type

Maps pandas column type to BigQuery column types. 

```python
_def __map_pandas_col_type_to_bq_type(self, col_type)
```

**Arguments**:

- `col_type`: pandas column type

**Returns**:

- `str`: BigQuery column type.


## **Usage**

```python
from lolpop.component import BigQueryDataConnector 

config = { 
    #insert component config here
}

# create instance of BigQueryDataConnector
bq = BigQueryDataConnector(conf=config)

# retrieve data from a table
data = bq.get_data("table_name")

# save data to a table
bq.save_data(data, "new_table_name")
```

In the example above, `config` is a dictionary with the required configuration information for Google BigQuery. The `get_data` method fetches data from the table named "table_name" and the `save_data` method saves the fetched data to a table named "new_table_name" in BigQuery.