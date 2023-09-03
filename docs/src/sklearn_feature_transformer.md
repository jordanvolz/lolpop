# sklearnFeatureTransformer

This class is a subclass of `BaseFeatureTransformer` and is used for transforming input data using scikit-learn transformers. It provides methods for fitting and transforming the data.

## Configuration
### Required Configuration

`sklearnFeatureTransformer` contains the following required configuration: 

- `transformers`: A list of transformers to run. Each transformer is a dictionary with the following entries: 
    - `transformer`: The `sklearn.preprocessing` class to use as the transformer. Required. 
    - `transformer_args`: A list of arguments to pass into the transformer. Optional.
    - `transformer_kwargs`: A dictionary of keyword arguments to pass into the transformer. Optional.
    - `transformer_columns`: A list of columns names to apply the transformer to. 

### Optional Configuration 

`sklearnFeatureTransformer` contains no optional configuration. 



### Default Configuration 

 `sklearnFeatureTransformer` contains the following default configuration:

- `column_transformer_kwargs`: A dictionary of keyword arguments to pass into the `ColumnTransformer` class. By default, this contains `{'remainder': 'passthrough'}`, which explicitly instructs the `ColumnTransformer` to pass through any columns in the dataset untransformed that are not mentioned in the `transformers` dictionary. If you override this, note that the default behavior for `ColumnTransformer` is to drop these columns. 

## Attributes

- `transformer` : An instance of `sklearn.compose.ColumnTransformer`, which is used to run all the transformers provided in the configuraiton. 


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

- `self.transformer`: The fitted `ColumnTransformer` object.


#### transform 
This method applies the fitted feature transformer to transform the input data.

```python 
def transform(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (array-like): The input data to be transformed.
- `**kwargs` (optional): Keyword arguments to be passed to the `transform` method.

**Returns**:

- `numpy.ndarray` or `scipy.sparse matrix`: The transformed data.


#### fit_transform
This method fits the feature transformer to the data and transforms it.

```python 
def fit_transform(self, data, *args, **kwargs)
```

**Arguments**:

- `data` (array-like): The input data to fit the transformer to and transform.
- `**kwargs` (optional): Keyword arguments to be passed to the `fit_transform` method.

**Returns**:

- `numpy.ndarray` or `scipy.sparse matrix`: The transformed data.

#### _get_transformer 
This method gets the scikit-learn transformer object based on the given class name.

```python
def _get_transformer(self, transformer_class, *args, **kwargs)
```

**Arguments**:

- `transformer_class`: The class name of the transformer.
- `**kwargs` (optional): Keyword arguments to be passed to the transformer constructor.

**Returns**:

- `object`: The instantiated scikit-learn transformer object.


## Usage:
```python
from lolpop.component import sklearnFeatureTransformer 

data = #generate data 

conf = {
    #insert component configuration here ... 

    "config" : {
        "transformers" : [
            {"transformer": "MinMaxScaler",
            "transformer_columns": ["height", "weight"]},
            {"transformer": "OneHotEncoder",
            "transformer_columns": ["sex", "state"]},
        ]
    }
}

transformer = sklearnFeatureTransformer(conf=conf)
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
		{"transformer": "MinMaxScaler", "transformer_columns": ["Height", "Weight", "Diameter"]},
		]
	}
}
```