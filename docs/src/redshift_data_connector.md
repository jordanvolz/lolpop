# RedshiftDataConnector Class

This Python class is used to establish a connection between Python and Amazon Redshift's data warehouse service. It is a subclass of the `PostgresDataConnector` class, inheriting its properties and methods.

This class allows for the management of a Redshift cluster and to perform data-related tasks such as querying, insertion, and deletion.

## Class Methods

### `__init__(self, *args, **kwargs)`

Class constructor method that initializes an instance of the `RedshiftDataConnector` class. It calls the constructor method of its parent class, `PostgresDataConnector`, passing in the same arguments as passed to this method.

This constructor method also loads the Redshift configuration details such as host, port, user, password, dbname, and schema, from a configuration file using the `load_config()` method from the `utils` module.

Example usage:
```python
connector = RedshiftDataConnector("redshift", config="redshift_config.yml")
```

### `__REQUIRED_CONF__` (class attribute)

This class attribute is a dictionary containing the list of configuration keys which are required to create an instance of this class. It checks if the configuration file contains all of the necessary information before creating an instance.

Example usage:
```python
class_config = {
    "REDSHIFT_HOST": "redshift-host.amazonaws.com",
    "REDSHIFT_PORT": "5439",
    "REDSHIFT_USER": "admin",
    "REDSHIFT_PASSWORD": "password",
    "REDSHIFT_DBNAME": "my_db",
    "REDSHIFT_SCHEMA": "public"
}
assert all(k in class_config for k in RedshiftDataConnector.__REQUIRED_CONF__["config"])
```

## Inherited Methods

This class has access to all of the methods inherited from its parent class, `PostgresDataConnector`. These include:

- `query(self, query: str, params: tuple = ())` - Executes a single SQL query and returns the result as a pandas DataFrame.
- `execute(self, query: str, params: tuple = ())` - Executes a single SQL statement that does not return any result.
- `commit(self)` - Commits the current transaction.
- `rollback(self)` - Rolls back the current transaction.
- `insert(self, table_name: str, data: pd.DataFrame, if_exists: str = "fail")` - Inserts rows to a table in the database.
- `truncate(self, table_name: str)` - Deletes all rows of a table in the database.
- `drop_table(self, table_name: str)` - Drops a table from the database.

Example usage:
```python
connector.query("SELECT * FROM my_table WHERE col1='foo'")
```