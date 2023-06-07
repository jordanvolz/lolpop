# **Class: BigQueryDataConnector**
## **Description**

This class is a child of the BaseDataConnector class and can be used to connect to Google BigQuery. It provides methods to retrieve data from a table or using raw SQL commands as well as to save data to a BigQuery table.

## Configuration 

### Required Configuration

### Optional Configuration 

### Default Configuration 

## Methods

### `__init__(self, *args, **kwargs)`

This method is the constructor for the BigQueryDataConnector class. It loads the configuration required to connect to BigQuery into the `self.bigquery_config` class variable. 

### `get_data(self, table, sql=None, *args, **kwargs)`

This method retrieves data from a table or raw SQL commmand executed in BigQuery. 

#### **Params**

- `table`: (str) Name of the table to fetch data from.
- `sql`: (str) SQL command to execute

#### **Returns**

- `pandas.DataFrame`: fetched data

### `save_data(self, data, table, *args, **kwargs)`

This method saves the given data to a table in BigQuery.

#### **Params**

- `data`: (pandas.DataFrame) Data to be saved.
- `table`: (str) Name of the table to save the data in.

### `_load_data(self, sql, config)`

This method executes the given SQL command in BigQuery and returns the retrieved data. 

#### **Params**

- `sql`: (str) SQL command to execute.
- `config`: (dict) Configuration information for BigQuery.

#### **Returns**

- `pandas.DataFrame`: Fetched data from BigQuery.

### `_save_data(self, data, table_name, config)`

This method saves the given data to a table in BigQuery. 

#### **Params**

- `data`: (pandas.DataFrame) The data to save
- `table_name`: (str) Name of table to save data
- `config`: (dict) Configuration file for bigqury project.

### `_get_client(self, key_path, project)`

This method returns a BigQuery API client object.

#### **Params**

- `key_path`: (str) Path to BigQuery credentials file.
- `project`: (str) Google cloud project ID.

#### **Returns**

- `google.cloud.bigquery.client`: A client object for BigQuery.

### `_get_format(self, extension)`

This method returns the MIME content type for the given file format extension.

#### **Params**

- `extension`: (str) File extension.

#### **Returns**

- `str`: MIME type.

## **Usage**

```
# create instance of BigQueryDataConnector
bq = BigQueryDataConnector(config)

# retrieve data from a table
data = bq.get_data("table_name")

# save data to a table
bq.save_data(data, "new_table_name")
```

In the example above, `config` is a dictionary with the required configuration information for Google BigQuery. The `get_data` method fetches data from the table named "table_name" and the `save_data` method saves the fetched data to a table named "new_table_name" in BigQuery.