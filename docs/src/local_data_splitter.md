# LocalDataSplitter

This class provides a consistent and streamlined way of splitting datasets into training, validation, and testing subsets for use in machine learning models. The split_data method takes in a pandas dataframe as input and returns an organized dictionary with the split datasets as keys. The splitting can be accomplished with random sampling, but the class also allows users to manually split data based on a provided column of the dataframe. Furthermore, when dealing with time-series data, the class allows for splitting while maintaining chronological order. 

## Configuration 

### Required Configuration

- `model_target` (str): The column representing the model target, or label.
### Optional Configuration 
For classification and regression problems you can use the following: 

- `drop_columns` (list): Columns from the source dataset to drop before forming the training/validation/test data sets. 
- `split_column` (str): The column to use for a manual split of data. This column contains values that you wish to use to split the data. 
- `split_classes` (dict): A dictionary that maps column values to split datasets. I.E. something like {"train" : "train", "valid" : "valid", "test" : "test"}. This allows you to use arbitrary values in your manual split. This is required if split_column is provided. 

For time-series problem you can use the following; 

- `time_index` (str): The column representing the time dimension of the time-series. 
- `test_size` (int): The size of the test dataset. 
- `validation_size` (int): The size of the validation dataset. 

### Default Configuration 

- `split_ratio` (list): A list representing percentages to use for each data split: train, validation, and test (if used). Default is `[0.8, 0.2]`
- `sample_num` (int): Allows users to sample data instead of using the entire dataset. If not specified, the component will try to use the entire dataset. Default is `100000`
- `use_stratified` (bool): Whether or not to use stratified sampling. Default is `False`
- `include_test` (bool): Whether or not to include a test dataset. Default is `False`
## Methods

### split_data
Splits data into training, validation, and test datasets. 

```python
split_data(self, data, *args, **kwargs)
```

**Arguments**:

- `data`: pd.DataFrame The DataFrame to split

**Returns**:

- `data_out`: dict(pd.DataFrame) A dictionary with the following keys, depending on the provided configuration:
    - `X_train`: Features of the training dataset
    - `X_valid`: Features of the validation dataset
    - `y_train`: Labels of the training dataset
    - `y_valid`: Labels of the validation dataset
    - `X_test`: Features of the test/holdout dataset
    - `y_test`: Labels of the validation dataset


### get_train_test_dfs
Returns training and test datasets. 

```python
get_train_test_dfs(self, data, combine_xy=True, combine_train_valid=True)
```

**Arguments**:

- `data`: (dict(pd.DataFrame)) A dictionary with the split dataset as follows:
    - `X_train`: Features of the training dataset.
    - `y_train`: Labels of the training dataset.
    - `X_valid`: Features of the validation dataset.
    - `y_valid`: Labels of the validation dataset.
    - `X_test`: Features of the test/holdout dataset.
    - `y_test`: Labels of the validation dataset.

- `combine_xy`: (bool) Whether to combine features with the model label. Default: True.

- `combine_train_valid`: (bool) Whether to combine training and validation datasets. Default: True.

**Returns**:

- (`train`, `test`): tuple(pd.DataFrame) A tuple with the resulting dataframes:
    - `train`: Contains the combined training and validation sets, if specified:
        - `X_`: Features of the training dataset.
        - `y_train`: Labels of the training dataset.
    - `test`: Contains the test/holdout dataset, if specified:
        - `X_test`: Features of the test/holdout dataset.
        - `y_test`: Labels of the validation dataset.

### _split_data()
Performs a split on non-time-series data. 

```python
_split_data(self, data, target,  split_column=None, split_classes={},  split_ratio=[0.8,0.2], sample_num=100000, use_startified=False, include_test=False, reset_index=True) 
```

**Arguments**:

- `data`: (pd.DataFrame) The DataFrame to split.
- `target`: (string) The model target or label.
- `split_column`: (string) The name of the column to use to manually split the data. Default: None.
- `split_classes`: (dict(string)) A dictionary mapping column values to determine the split datasets. Only used when split_column is specified. Default: {}.
- `split_ratio`: (list(float)) The ratio of rows to include in dataframes. This should contain either 2 or 3 floats representing the train, valid, and test datasets, respectively. Must add up to 1. Default: [0.8,0.2].
- `sample_num`: (int)The number of rows to include in all the split datasets. Default: 100000.
- `use_startified`: (bool)Whether to use stratified sampling. Default: False.
- `include_test`: (bool) Whether to include a test/holdout dataset. Default: False.
- `reset_index`: (bool) Whether to reset the index for resulting dataframes. Default: True.

**Returns**:

- `data_out`: (dict(pd.DataFrame)) A dictionary of the following dataframes:
    - `X_train`: Features of the training dataset.
    - `y_train`: Labels of the training dataset.
    - `X_valid`: Features of the validation dataset.
    - `y_valid`: Labels of the validation dataset.
    - `X_test`: Features of the test/holdout dataset.
    - `y_test`: Labels of the validation dataset.

### _split_timeseries_data
Performs a split on timeseries data. 

```python
_split_timeseries_data(self, data, time_index, target, test_size=0, validation_size=0)
```

**Arguments**:

- `data`: (pd.DataFrame) The DataFrame to split
- `time_index`: (string) The name of the column in the DataFrame containing time data.
- `target`: (string) The model target or label.
- `test_size`: (int) The number of rows to be used in the test set. Assumes data is sorted chronologically.
- `validation_size`: (int) The number of rows to be used in the validation set. Assumes data is sorted chronologically.

**Returns**:

- `data_out` dict(pd.DataFrame): A dictionary of the following dataframes:
    - `X_train`: Features of the training dataset.
    - `y_train`: Labels of the training dataset.
    - `X_valid`: Features of the validation dataset.
    - `y_valid`: Labels of the validation dataset.


### _build_split_dfs
Helper function to build the dictionary object for training, validation, and test datasets. 

```python
_build_split_dfs(self, train, valid, target,  split_column="SPLIT", test=None, reset_index=True)
```
**Arguments**:

- `train`: (pd.DataFrame) The training dataset.
- `valid`: (pd.DataFrame) The validation dataset.
- `target`: (string) The model target or label.
- `split_column`: (string) The name of the column containing the split data. Default: 'SPLIT'.
- `test`: (pd.DataFrame) The test/holdout dataset. Default: None.
- `reset_index`: (bool) Whether to reset the index for resulting dataframes. Default: True.

**Returns**:

- `data_out`: (dict(pd.DataFrame)) A dictionary with the following dataframes:
    - `X_train`: Features of the training dataset.
    - `y_train`: Labels of the training dataset.
    - `X_valid`: Features of the validation dataset.
    - `y_valid`: Labels of the validation dataset.
    - `X_test`: Features of the test/holdout dataset.
    - `y_test`: Labels of the validation dataset.

## Usage


Here is a simple example of implementing the LocalDataSplitter class:

```python
from lolpop.component import LocalDataSplitter

config = {
    #insert component configuration here
}

# Instantiate a data splitter object
data_splitter = LocalDataSplitter(conf=config)

# Read in the input data from file
input_data = pd.read_csv('input_data.csv')

# Split the data according to the provided configuration
split_dataset = data_splitter.split_data(input_data) 

# Extract the training data for use in a machine learning model
X_train = split_dataset.get('X_train')
y_train =split_dataset.get('y_train')

```