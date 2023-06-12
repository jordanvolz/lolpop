# **Class: LocalDataSplitter**

This class provides a consistent and streamlined way of splitting datasets into training, validation, and testing subsets for use in machine learning models. The split_data method takes in a pandas dataframe as input and returns an organized dictionary with the split datasets as keys. The splitting can be accomplished with random sampling, but the class also allows users to manually split data based on a provided column of the dataframe. Furthermore, when dealing with time-series data, the class allows for splitting while maintaining chronological order. 

## Usage

### **Example**

Here is a simple example of implementing the LocalDataSplitter class:

```python
from LocalDataSplitter import LocalDataSplitter

# Instantiate a data splitter object
data_splitter = LocalDataSplitter()

# Read in the input data from file
input_data = pd.read_csv('input_data.csv')

# Split the data according to the provided configuration
split_dataset = data_splitter.split_data(input_data) 

# Extract the training data for use in a machine learning model
X_train = split_dataset.get('X_train')
y_train =split_dataset.get('y_train')

```

## Methods

### **split_data()**

```python
split_data(self, data, **kwargs)
```

##### Arguments:

- data: pd.DataFrame
    - The DataFrame to split

##### Returns:
- data_out: dict(pd.DataFrame)
    - A dictionary with the following keys, depending on the provided configuration:
        - X_train: Features of the training dataset
        - X_valid: Features of the validation dataset
        - y_train: Labels of the training dataset
        - y_valid: Labels of the validation dataset
        - X_test: Features of the test/holdout dataset
        - y_test: Labels of the validation dataset


### **_split_timeseries_data()**
```python
_split_timeseries_data(self, data, time_index, target, test_size=0, validation_size=0)
```

##### Arguments:

- data: pd.DataFrame
    - The DataFrame to split

- time_index: string
    - The name of the column in the DataFrame containing time data.

- target: string
    - The model target or label.

- test_size: int
    - The number of rows to be used in the test set. Assumes data is sorted chronologically.

- validation_size: int
    - The number of rows to be used in the validation set. Assumes data is sorted chronologically.

##### Returns:
- data_out: dict(pd.DataFrame)
    - A dictionary of the following dataframes:
        - X_train: Features of the training dataset.
        - y_train: Labels of the training dataset.
        - X_valid: Features of the validation dataset.
        - y_valid: Labels of the validation dataset.


### **_split_data()**
```python
_split_data(self, data, target,  split_column=None, split_classes={},  split_ratio=[0.8,0.2], sample_num=100000, use_startified=False, include_test=False, reset_index=True) 
```

##### Arguments:

- data: pd.DataFrame
    - The DataFrame to split.

- target: string
    - The model target or label.

- split_column: string, optional
    - The name of the column to use to manually split the data. Default: None.

- split_classes: dict(string), optional
    - A dictionary mapping column values to determine the split datasets. Only used when split_column is specified. Default: {}.

- split_ratio: list(float), optional
    - The ratio of rows to include in dataframes. This should contain either 2 or 3 floats representing the train, valid, and test datasets, respectively. Must add up to 1. Default: [0.8,0.2].

- sample_num: int, optional
    - The number of rows to include in all the split datasets. Default: 100000.

- use_startified: bool, optional
    - Whether to use stratified sampling. Default: False.

- include_test: bool, optional
    - Whether to include a test/holdout dataset. Default: False.

- reset_index: bool, optional
    - Whether to reset the index for resulting dataframes. Default: True.

##### Returns:
- data_out: dict(pd.DataFrame)
    - A dictionary of the following dataframes:
        - X_train: Features of the training dataset.
        - y_train: Labels of the training dataset.
        - X_valid: Features of the validation dataset.
        - y_valid: Labels of the validation dataset.
        - X_test: Features of the test/holdout dataset.
        - y_test: Labels of the validation dataset.


### **_build_split_dfs()**
```python
_build_split_dfs(self, train, valid, target,  split_column="SPLIT", test=None, reset_index=True)
```

##### Arguments:

- train: pd.DataFrame
    - The training dataset.

- valid: pd.DataFrame
    - The validation dataset.

- target: string
    - The model target or label.

- split_column: string, optional
    - The name of the column containing the split data. Default: 'SPLIT'.

- test: pd.DataFrame, optional
    - The test/holdout dataset. Default: None.

- reset_index: bool, optional
    - Whether to reset the index for resulting dataframes. Default: True.

##### Returns:
- data_out: dict(pd.DataFrame)
    - A dictionary with the following dataframes:
        - X_train: Features of the training dataset.
        - y_train: Labels of the training dataset.
        - X_valid: Features of the validation dataset.
        - y_valid: Labels of the validation dataset.
        - X_test: Features of the test/holdout dataset.
        - y_test: Labels of the validation dataset.

### **get_train_test_dfs()**
```python
get_train_test_dfs(self, data, combine_xy=True, combine_train_valid=True)
```

##### Arguments:

- data: dict(pd.DataFrame)
    - A dictionary with the split dataset as follows:
        - X_train: Features of the training dataset.
        - y_train: Labels of the training dataset.
        - X_valid: Features of the validation dataset.
        - y_valid: Labels of the validation dataset.
        - X_test: Features of the test/holdout dataset.
        - y_test: Labels of the validation dataset.

- combine_xy: bool, optional
    - Whether to combine features with the model label. Default: True.

- combine_train_valid: bool, optional
    - Whether to combine training and validation datasets. Default: True.

##### Returns:
- (train, test): tuple(pd.DataFrame)
    - A tuple with the resulting dataframes:
        - train: Contains the combined training and validation sets, if specified:
            - X_: Features of the training dataset.
            - y_train: Labels of the training dataset.
        - test: Contains the test/holdout dataset, if specified:
            - X_test: Features of the test/holdout dataset.
            - y_test: Labels of the validation dataset.