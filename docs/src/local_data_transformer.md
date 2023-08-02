# LocalDataTransformer

The `LocalDataTransformer` class is a subclass of `BaseDataTransformer` and is used for transforming local data using user-defined local transformer functions. The class has the following methods:

## Configuration
### Required Configuration

- `transformer_path`: The filepath to the transformer file.  

### Optional Configuration 

- `data_connector_config`: The configuration to pass into the data connector class. 
### Default Configuration 

- `transformer_func`: The function in the transformer file to use to transform the data. Defaults to `transform`. 
- `data_connector`: The `data_connector` class to user to load data. Defaults to `LocalDataConnector`. 

## Attributes

- `_transform` : This is the loaded `transformer_func`. 


## Methods

### __init__ 
This method initializes the `LocalDataTransformer` class. It loads the transformer function and data connector to be used in the transformation process. The transformer function and path to the transformer file are retrieved from the configuration settings. If the transformer file exists, the transformer function will be loaded. The data connector configuration is also retrieved, and the data connector is instantiated.



### transform 
This method allows for local transformer workflow to be run in python. It takes `input_data` as a parameter, and it returns a `pd.DataFrame` of the transformed data.

```python 
transform(self, input_data, *args, **kwargs)
```



**Arugments**: 

- `input_data` (string): names of file to load and pass to transformer file.

**Returns**: 

- `pd.DataFrame`: the transformed data

## Usage

```python
from lolpop.component import LocalDataTransformer

config = {
    #insert component config here
}

local_transformer = LocalDataTransformer(conf = config)

transformed_data = local_transformer.transform(data)
```

