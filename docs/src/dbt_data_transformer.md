# Class Documentation: dbtDataTransformer

The `dbtDataTransformer` class provides functionality to transform data using the [dbt (data build tool)](https://docs.getdbt.com/docs/introduction). It inherits from the `BaseDataTransformer` class to make use of its properties.

## Class Attributes

### __REQUIRED_CONF__

The `__REQUIRED_CONF__` class attribute is a dictionary that contains the required configuration parameters for initializing the `dbtDataTransformer` class. It has the following key-value pairs:
* `"config"`: A list of strings representing the names of the keys in the `config` object of the class instance. The `config` object contains configuration variables required for the class to function properly.


## Class Methods

### __init__(self, components={}, *args, **kwargs)

The `__init__` method initializes an instance of the `dbtDataTransformer` class. It accepts the following parameters:
* `components`: A dictionary object containing any dependent component classes required by the `dbtDataTransformer` class. A component is an optional class that performs a specific data transformation. The default value is an empty dictionary.
* `*args, **kwargs`: Arbitrary arguments and keyword arguments to pass on to the parent class constructor.

### transform(self, source_table_name, *args, **kwargs)

The `transform` method transforms data using a dbt workflow specified in the dbt configuration provided. It has the following parameters:
* `source_table_name`: A string representing the name of the table to load and return. This should be a table created in the dbt workflow.
* `*args, **kwargs`: Arbitrary arguments and keyword arguments to pass to the method.

The `transform` method returns a Pandas DataFrame representing the transformed data.

## Example Usage

```python
# Instantiate a dbtDataTransformer object with any necessary configurations
dt = dbtDataTransformer(config={
    "data_connector": "my_data_connector",
    "DBT_TARGET": "production",
    "DBT_PROFILE": "my_profile",
    "DBT_PROJECT_DIR": "/path/to/project",
    "DBT_PROFILES_DIR": "/path/to/profiles"
})

# Call the transform method to retrieve and transform data from a dbt workflow
transformed_data = dt.transform("my_table")
```