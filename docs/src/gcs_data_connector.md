# GCSDataConnector

The `GCSDataConnector` class is a Python class that provides an interface for loading data from and saving data to Google Cloud Storage. It is a subclass of the `BaseDataConnector` class and is designed to work with Pandas data frames. `GCSDataConnector` utilizes the Google Cloud Storage Python API and the Pandas library to implement the functionality of loading and saving data.

## Methods

### `__init__(self, *args, **kwargs)`

The constructor of the `GCSDataConnector` class. It sets the parameters for the client used to access Google Cloud Storage. 

### `get_data(self, path, *args, **kwargs)`

Load data from the given Google Cloud Storage path and return as a Pandas DataFrame.

#### Parameters
- `path`: str
    - Path of the file to be loaded.

#### Returns
- `pd.DataFrame`
    - DataFrame with the loaded data.

#### Example
```
connector = GCSDataConnector()
df = connector.get_data('gs://example-bucket/example.csv')
```

### `save_data(self, data, path, *args, **kwargs)`

Save the provided data to the given Google Cloud Storage path.

#### Parameters
- `data`: pd.DataFrame
    - DataFrame to be saved.
- `path`: str
    - Path where the file will be saved.

#### Returns
- `None`

#### Example
```
connector = GCSDataConnector()
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
connector.save_data(df, 'gs://example-bucket/example.parquet')
```

### `_load_data(self, path, keyfile, project, **kwargs)`

Load data from the given Google Cloud Storage path and return as a Pandas DataFrame.

#### Parameters
- `path`: str
    - Path of the file to be loaded.
- `keyfile`: str
    - Path to the Google Cloud Storage service account file.
- `project`: str
    - Name of the Google Cloud Storage project.

#### Returns
- `pd.DataFrame`
    - DataFrame with the loaded data.

### `_save_data(self, data, path, keyfile, project, *args, **kwargs)`

Save the provided data to the given Google Cloud Storage path.

#### Parameters
- `data`: pd.DataFrame
    - DataFrame to be saved.
- `path`: str
    - Path where the file will be saved.
- `keyfile`: str
    - Path to the Google Cloud Storage service account file.
- `project`: str
    - Name of the Google Cloud Storage project.

#### Returns
- `None`

### `_get_client(self, key_path, project)`

Return a Google Cloud Storage client authenticated using the provided credentials.

#### Parameters
- `key_path`: str
    - Path to the Google Cloud Storage service account file.
- `project`: str
    - Name of the Google Cloud Storage project.

#### Returns
- `storage.Client`
    - Authenticated GSC client object.

### `_get_format(self, extension)`

Returns the MIME type for the provided file extension.

#### Parameters
- `extension`: str
    - File extension.

#### Returns
- `str`
    - MIME type.

## Usage

Here is an example of how to use the `GCSDataConnector` class to load and save data from Google Cloud Storage.

```
from GCSDataConnector import GCSDataConnector
import pandas as pd

# Load data from Google Cloud Storage
connector = GCSDataConnector()
df = connector.get_data('gs://example-bucket/example.csv')

# Save data to Google Cloud Storage
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
connector.save_data(df, 'gs://example-bucket/example.parquet')
```