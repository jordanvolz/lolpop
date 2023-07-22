# LocalDataConnector

This is a Python class that inherits from `BaseDataConnector` class and provides methods to read and write CSV, parquet, or ORC file to local storage. The class has two main methods `get_data()` and `save_data()`.

## Configuration

### Required Configuration

There is no required configuration.

### Optional Configuration 

There is not optional configuration. 

### Default Configuration 
There is no default configuration. 

## Methods:
### get_data 
This method reads data from the specified file path (CSV, Parquet, or ORC) into memory as a pandas DataFrame. The method returns the loaded data as a pandas DataFrame. The loaded file is read using the Pyarrow engine which supports the reading of these file formats. 

```python 
def get_data(self, source_path, *args, **kwargs)
```

**Arguments**:

- `source_path` (str): The path to the data source file.

**Returns**:

- `pandas.DataFrame`: Returns data as a pandas DataFrame.

**Example**:

```python
import pandas as pd
from lolpop.component import LocalDataConnector

config = {
    #insert component config here
}

# Create an instance of LocalDataConnector
connector = LocalDataConnector(conf=config)

# Data file path
data_path = "/datafolder/sales/sales_data.csv"

# Load the data into a pandas dataframe
data = connector.get_data(data_path)

# Display the first 5 rows of the data
print(data.head(5))
```

### save_data 
This method writes data from a pandas DataFrame into a specified file path as CSV or Parquet format and returns the saved data. 

```python 
def save_data(self, data, target_path, *args, **kwargs)

```

**Arguments**:

- `data` (pandas.DataFrame): Data to be saved.

- `target_path` (str): The path to the target file.


**Returns**:

- `pandas.DataFrame`: Returns saved data.

**Example**:

```python
import pandas as pd
from lolpop.component import LocalDataConnector

config = {
    #insert component config here
}

# Create an instance of LocalDataConnector
connector = LocalDataConnector(conf=config)

# Load sample data into pandas DataFrame
data = pd.DataFrame({
    "product_name": ["Product A", "Product B", "Product C"],
    "quantity_sold": [100, 200, 300],
    "revenue": [2500, 5000, 7500]
})

# Define file path to save the data
save_path = "/data/sales/sales_data.csv"

# Save the data to the specified file path
connector.save_data(data, save_path)

```