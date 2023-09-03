# FeatureEngineFeatureTransformer

This class is a subclass of `BaseFeatureTransformer` and is used for transforming input data using `feature_engine` transformers. It provides methods for fitting and transforming the data.

## Configuration
### Required Configuration

`FeatureTransformerFeatureTransformer` contains the following configuration: 

- `transformers`: A list of transformers to run. Each transformer is a dictionary with the following entries: 
    - `transformer`: The `feature_engine` class to use as the transformer. Required. 
    - `transformer_args`: A list of arguments to pass into the transformer. Optional.
    - `transformer_kwargs`: A dictionary of keyword arguments to pass into the transformer. Optional.
    - `transformer_columns`: A list of columns names to apply the transformer to. 

### Optional Configuration 

`FeatureTransformerFeatureTransformer` contains the following optional configuration: 

- `pipeline_kwargs`: A dictionary of keyword arguments to pass into the `sklearn.pipline.Pipeline` object that is used to pipeline together the `feature_engine` transformations. 


### Default Configuration 

 `FeatureTransformerFeatureTransformer` contains no default configuration.

## Attributes

- `transformer` : An instance of `sklearn.pipeline.Pipeline`, which is used to run all the transformers provided in the configuration. 


## Methods 


#### fit 

This method fits the feature transformer to the input data.

```python 
def fit(self, data, *args, **kwargs)
```


**Arguments**:

- `data` (array-like): The input data to fit the transformer to.
- `**kwargs` (optional): Keyword arguments to be passed to the `fit` method.

**Returns**:

- `self.transformer`: The fitted `Pipeline` object.


#### transform 
This method applies the fitted feature transformer to transform the input data.

```python 
def transform(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (array-like): The input data to be transformed.
- `**kwargs` (optional): Keyword arguments to be passed to the `transform` method.

**Returns**:

- A dataframe containing the transformed data. 


#### fit_transform
This method fits the feature transformer to the data and transforms it.

```python 
def fit_transform(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (array-like): The input data to fit the transformer to and transform.
- `**kwargs` (optional): Keyword arguments to be passed to the `fit_transform` method.

**Returns**:

- A dataframe containing the transformed data. 


#### _get_transformer 
This method gets the `feature_engine` transformer object based on the given class name.

```python
def _get_transformer(self, transformer_class, columns, *args, **kwargs)
```

**Arguments**:

- `transformer_class`: The class name of the transformer.
- `columns`: The columns to apply the transformer to
- `**kwargs` (optional): Keyword arguments to be passed to the transformer constructor.

**Returns**:

- `object`: The instantiated `feature_engine` transformer object.


#### _map_transformer 
This method maps the `feature_engine` class name to the `feature_engine` object.

```python
def _map_transformer(self, transformer_class)
```

**Arguments**:

- `transformer_class`: The class name of the transformer.

**Returns**:

- `object`: The `feature_engine` class.



## Usage:
```python
from lolpop.component import FeatureTransformerFeatureTransformer 

data = #generate data 

conf = {
    #insert component configuration here ... 

    "config" : {
        "transformers" : [
            {"transformer": "OneHotEncoder", "transformer_columns": ["Sex"]},
            {"transformer": "LogCpTransformer", "transformer_columns": ["Height", "Weight", "Diameter"]},
        ]
    }
}

transformer = FeatureTransformerFeatureTransformer(conf=conf)
transformed_data = transformer.fit_transform(data)

print(transformed_data)
```

### Sample Configuration 

```python 
conf = {
	"config": {
		"transformers": 
		[
            {"transformer": "OneHotEncoder", "transformer_columns": ["Sex"]},
            {"transformer": "LogCpTransformer", "transformer_columns": ["Height", "Weight", "Diameter"]},
		]
	}
}
```