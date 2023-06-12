# Class: LocalDataConnector

This is a Python class that inherits from `BaseDataConnector` class and provides methods to read and write CSV, parquet, or ORC file to local storage. The class has two main methods `get_data()` and `save_data()`.

## Methods:
### 1. get_data(self, source_path, *args, **kwargs)

This method reads data from the specified file path (CSV, Parquet, or ORC) into memory as a pandas DataFrame. The method returns the loaded data as a pandas DataFrame. The loaded file is read using the Pyarrow engine which supports the reading of these file formats. 

#### Input parameters:

    - source_path (str): The path to the data source file.

    - *args: Optional position arguments that can be passed to the pandas methods.

    - **kwargs: Optional keyword arguments that can be passed to the pandas methods.

#### Output:
    - pandas.DataFrame: Returns data as a pandas DataFrame.

#### Example:

```python
import pandas as pd
from LocalDataConnector import LocalDataConnector

# Create an instance of LocalDataConnector
connector = LocalDataConnector()

# Data file path
data_path = "/datafolder/sales/sales_data.csv"

# Load the data into a pandas dataframe
data = connector.get_data(data_path)

# Display the first 5 rows of the data
print(data.head(5))
```

### 2. save_data(self, data, target_path, *args, **kwargs)

This method writes data from a pandas DataFrame into a specified file path as CSV or Parquet format and returns the saved data. 

#### Input parameters:

    - data (pandas.DataFrame): Data to be saved.

    - target_path (str): The path to the target file.

    - *args: Optional position arguments that can be passed to the to_csv or to_parquet methods.

    - **kwargs: Optional keyword arguments that can be passed to the to_csv or to_parquet methods.

#### Output:
    - pandas.DataFrame: Returns saved data.

#### Example:

```python
import pandas as pd
from LocalDataConnector import LocalDataConnector

# Create an instance of LocalDataConnector
connector = LocalDataConnector()

# Load sample data into pandas DataFrame
data = pd.DataFrame({
    "product_name": ["Product A", "Product B", "Product C"],
    "quantity_sold": [100, 200, 300],
    "revenue": [2500, 5000, 7500]
})

# Define file path to save the data
save_path = "/datafolder/sales/sales_data.csv"

# Save the data to the specified file path
connector.save_data(data, save_path)

```