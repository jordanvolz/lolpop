# dbtDataTransformer

The `dbtDataTransformer` class provides functionality to transform data using [dbt (data build tool)](https://docs.getdbt.com/docs/introduction). It inherits from the `BaseDataTransformer` class to make use of its properties.

## Configuration

### Required configuration 

- `DBT_PROFILE`: The profile to use. 
- `DBT_TARGET` : The target to use in the profile. 
- `DBT_PROJECT_DIR` : The filepath to the dbt project. 
- `DBT_PROFILES_DIR` : The filepath to the dbt profile.  
- `data_connector`: The data connector class to use to load data after the dbt job has completed. DBT doesn't itself return data, so we need to fetch it after it completes. This should be the data_connector class of the data warehouse you use to run your dbt job.  

## Class Methods

###  __init__

The `__init__` method initializes an instance of the `dbtDataTransformer` class. dbt loads a `data_connector` to load data after the dbt run has completed. It will fetch the connection information from the provided dbt profile. 


### transform 
The `transform` method transforms data using a dbt workflow specified in the dbt configuration provided.

```python 
def transform(self, source_table_name, *args, **kwargs)
```

**Arguments**: 

* `source_table_name`: A string representing the name of the table to load and return. This should be a table created in the dbt workflow.
* `*args, **kwargs`: Arbitrary arguments and keyword arguments to pass to the method.

**Returns**: 

The `transform` method returns a Pandas DataFrame representing the transformed data.

## Usage

```python
from lolpop.component import dbtDataTransformer 

config = {
    #insert component config here 
}

dt = dbtDataTransformer(conf=config)

# Call the transform method to retrieve and transform data from a dbt workflow
transformed_data = dt.transform("my_table")
```