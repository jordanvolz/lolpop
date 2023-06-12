# LocalDataTransformer

The `LocalDataTransformer` class is a subclass of `BaseDataTransformer` and is used for transforming local data using user-defined local transformer functions. The class has the following methods:

## `__init__(self, components={}, *args, **kwargs)`

This method initializes the `LocalDataTransformer` class. It loads the transformer function and data connector to be used in the transformation process. The transformer function and path to the transformer file are retrieved from the configuration settings. If the transformer file exists, the transformer function will be loaded. The data connector configuration is also retrieved, and the data connector is instantiated.

### Parameters:
- `components` (dict): a dictionary of components to be passed to the class
- `*args`: variable length argument list
- `**kwargs`: variable length keyword argument list

## `transform(self, input_data, *args, **kwargs)`

This method allows for local transformer workflow to be run in python. It takes `input_data` as a parameter, and it returns a `pd.DataFrame` of the transformed data.

### Parameters:
- `input_data` (string): names of file to load and pass to transformer file.

### Returns:
- `pd.DataFrame`: the transformed data

## Examples
### Importing the class

```python
from path.to.file import LocalDataTransformer
```

### Creating an instance of the LocalDataTransformer

```python
local_transformer = LocalDataTransformer()
```

### Running the transform method

```python
data = {'file1': '/path/to/file1.csv', 'file2': '/path/to/file2.csv'}
transformed_data = local_transformer.transform(data)
```

In this example, `file1.csv` and `file2.csv` are loaded and passed to the transformer function, and the output is a transformed DataFrame.