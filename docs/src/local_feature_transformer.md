# LocalFeatureTransformer

The `LocalFeatureTransformer` class is a subclass of `BaseFeatureTransformer` and provides methods to fit and transform data using a feature transformer. Your local transformer should implement the following functions: 

- `fit(self, config, X_data, y_data, *args, **kwargs)`
- `transform(self, config, data, *args, **kwargs)`

Note that the component configuration is passed into each method. 

## Configuration
### Required Configuration

`LocalFeatureTransformer` contains the following required configuration: 

- `feature_transformer_path`: The path to the python module to use to transform features. 
- `transformer_class`: The class in the python module to use as the feature transformer. 

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


### transform 
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


### fit_transform 
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

## Sample Local Transformer

```python 
from sklearn.preprocessing import OneHotEncoder
import pandas as pd 

class MyTransformer(): 

    def fit(self, config, X_data, y_data, *args, **kwargs): 
        categorical_cols = config.get("categorical_columns")
        #encode categories
        self.ft = OneHotEncoder(handle_unknown="ignore")
        self.ft.fit(X_data[categorical_cols])
        return self.ft
    
    def transform(self, config, data, *args, **kwargs):
        categorical_cols = config.get("categorical_columns")
        transformed_data = self.ft.transform(data[categorical_cols]) 
        transformed_df = pd.DataFrame(transformed_data.toarray(), columns=self.ft.get_feature_names_out())
        data_out = pd.concat([transformed_df, data.drop(columns=categorical_cols)], axis=1)
        return data_out

```