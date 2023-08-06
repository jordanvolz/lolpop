# RedshiftDataConnector

This Python class is used to establish a connection between Python and Amazon Redshift's data warehouse service. It is a subclass of the `PostgresDataConnector` class, inheriting its properties and methods.

This class allows for the management of a Redshift cluster and to perform data-related tasks such as querying, insertion, and deletion.

## Configuration 

### Required Configuration

- `REDSHIFT_HOST`: Hostname of the Redshift db.
- `REDSHIFT_PORT`: Port used by the Redshift db.
- `REDSHIFT_USER`: User to use to connect to the Redshift db.
- `REDSHIFT_PASSWORD`: Password for `REDSHIFT_USER`.
- `REDSHIFT_DBNAME`: Redshift database to use to load/save data. 
- `REDSHIFT_SCHEMA`: Default Redshift schema to use. 

### Optional Configuration 

There is no optional configuration. 

### Default Configuration 
There is no default configuration. 


## Methods

### `__init__`

Class constructor method that initializes an instance of the `RedshiftDataConnector` class. It calls the constructor method of its parent class, `PostgresDataConnector`, passing in the same arguments as passed to this method.

This constructor method also loads the Redshift configuration details such as host, port, user, password, dbname, and schema, from a configuration file using the `load_config()` method from the `utils` module.

!!! Note
    Since this is just a wrapper around the [PostgresDataConnector](postgres_data_connector.md), please see that documentation for all usable methods. 

Example usage:
```python
connector = RedshiftDataConnector(config="redshift_config.yml")
```


##  Usage:
```python
from lolpop.component import RedshiftDataConnector
import pandas as pd


config = {
    #insert component config here 
}

# Instantiate a PostgresDataConnector object
rsdc = RedshiftDataConnector(conf=config)

# Retrieve data from a table in the database
df = rsdc.get_data("my_table")

# Save data to a table in the database
new_data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
rsdc.save_data(new_data, "my_table2")

```