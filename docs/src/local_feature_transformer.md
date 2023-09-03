# LocalFeatureTransformer

The `LocalFeatureTransformer` class is a subclass of `BaseFeatureTransformer` and provides methods to fit and transform data using a feature transformer.

## Configuration
### Required Configuration

`LocalFeatureTransformer` contains the following required configuration: 

- `feature_transformer_path`: The path to the python module to use to transform features. 

### Optional Configuration 

`LocalFeatureTransformer` contains no optional configuration. 

### Default Configuration 

 `LocalFeatureTransformer` contains the following default configuration:

- `fit_func`: The name of the function in `feature_transformer_path` to use to fit the transformer to the data. Defaults to "fit". 
- `fit_params`: Optional parameters to use to pass into the `fit_func`. Defaults to `{}`. 
- `transform_func`: The name of the function to use to transform data using the fit feature transformer crated from `fit_func`. Defaults to "transform".
- `transform_params`: Optional parameters to use to pass into the `transform_func` when transforming data. Defaults to `{}`


## Methods

### fit 
Fits the feature transformer with the given data.


```python 
def fit(data, *args, **kwargs)
```

**Arguments:**

- `data`: The input data to fit the transformer.
- `*args`: Variable length argument list.
- `**kwargs`: Arbitrary keyword arguments.

**Returns:**

The fitted feature transformer.


#### transform 
Transforms the given data using the fitted feature transformer.

```python 
def transform(data, *args, **kwargs)
```


**Arguments:**

- `data`: The input data to transform.
- `*args`: Variable length argument list.
- `**kwargs`: Arbitrary keyword arguments.

**Returns:**

The transformed data.


#### fit_transform 
Fits the feature transformer with the given data and then transforms the data.

```python 
def fit_transform(data, *args, **kwargs)
```

**Arguments:**

- `data`: The input data to fit and transform.
- `*args`: Variable length argument list.
- `**kwargs`: Arbitrary keyword arguments.

**Returns:**

The transformed data.


## Usage

```python
from lolpop.component import LocalFeatureTransformer

conf = {
    #insert component configuration 
    config: {
        "feature_transformer_path": "/path/to/my_transformer.py"
    }
}

# Create an instance of LocalFeatureTransformer
transformer = LocalFeatureTransformer(conf=conf)

# Fit the transformer with data
data = ...
transformer.fit(data)

# Transform the data
transformed_data = transformer.transform(data)

print(transformed_data)
```