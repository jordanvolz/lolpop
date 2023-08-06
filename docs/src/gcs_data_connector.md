# GCSDataConnector

The `GCSDataConnector` class is a Python class that provides an interface for loading data from and saving data to Google Cloud Storage. It is a subclass of the `BaseDataConnector` class and is designed to work with Pandas data frames. `GCSDataConnector` utilizes the Google Cloud Storage Python API and the Pandas library to implement the functionality of loading and saving data.

## Configuration

### Required Configuration

- `GOOGLE_PROJECT`: The GCP project to connect to. 

### Optional Configuration 

- `GOOGLE_KEYFILE`: Location of a GCS credentials file to use in order to connect to GCS. If no keyfile is provided, the component will attempt to use the standard environment variable `GOOGLE_APPLICATION_CREDENTIALS`. 

### Default Configuration 
There is no default configuration. 

## Methods

### get_data

Load data from the given Google Cloud Storage path and return as a Pandas DataFrame.

```python
def get_data(self, path, *args, **kwargs)
```
**Arguments**

- `path`: (str) Path of the file to be loaded.

**Returns**

- `pd.DataFrame` DataFrame with the loaded data.

**Example**
```
from lolpop.component import GCSDataConnector

config = {
    #insert component config here
}

connector = GCSDataConnector(conf=config)

df = connector.get_data('gs://example-bucket/example.csv')
```

###  save_data 

Save the provided data to the given Google Cloud Storage path.

```python 
def save_data(self, data, path, *args, **kwargs)
```

**Arguments**

- `data`: (pd.DataFrame) DataFrame to be saved.
- `path`: (str) Path where the file will be saved.


**Example**
```
from lolpop.component import GCSDataConnector 

config = {
    #insert component config here 
}

connector = GCSDataConnector(conf=config)

df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

connector.save_data(df, 'gs://example-bucket/example.csv')
```

### _load_data
Load data from the given Google Cloud Storage path and return as a Pandas DataFrame.

```python 
def _load_data(self, path, keyfile, project, **kwargs)
```

**Arguments**

- `path`: (str) Path of the file to be loaded.
- `keyfile`: (str) Path to the Google Cloud Storage service account file.
- `project`: (str) Name of the Google Cloud Storage project.

**Returns**

- `pd.DataFrame` DataFrame with the loaded data.

### _save_data 
Save the provided data to the given Google Cloud Storage path.

```python 
def _save_data(self, data, path, keyfile, project, *args, **kwargs)
```

**Arguments**

- `data`: (pd.DataFrame) DataFrame to be saved.
- `path`: (str) Path where the file will be saved.
- `keyfile`: (str) Path to the Google Cloud Storage service account file.
- `project`: (str) Name of the Google Cloud Storage project.

### _get_client 
Return a Google Cloud Storage client authenticated using the provided credentials.

```python 
def _get_client(self, key_path, project)
```
**Arguments**

- `key_path`: (str) Path to the Google Cloud Storage service account file.
- `project`: (str) Name of the Google Cloud Storage project.

**Returns**

- `storage.Client`Authenticated GCS client object.

### _get_format 

Returns the MIME type for the provided file extension.

```python
def _get_format(self, extension)
```

**Arguments**

- `extension`: (str) File extension.

**Returns**

- `str` MIME type.

## Usage

Here is an example of how to use the `GCSDataConnector` class to load and save data from Google Cloud Storage.

```
from lolpop.component import GCSDataConnector
import pandas as pd

config = {
    #insert component configuration here
}

# Load data from Google Cloud Storage
connector = GCSDataConnector(conf=config)
df = connector.get_data('gs://example-bucket/example.csv')

# Save data to Google Cloud Storage
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
connector.save_data(df, 'gs://example-bucket/example.csv')
```