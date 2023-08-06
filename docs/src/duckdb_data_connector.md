# DuckDBDataConnector

This document explains the features of the DuckDBDataConnector class, which retrieves data from a DuckDB table or custom SQL provided and saves data to the specified table in the specified instance. This class extends from the BaseDataConnector class.

## Configuration

### Required Configuration

- `duckdb_path`: The filepath to the duckdb instance.  

### Optional Configuration 
There is no optional configuration.

### Default Configuration 
There is no default configuration. 


## Methods

### get_data

The get_data() method retrieves data from the DuckDBDataConnector table or custom SQL provided and returns a Pandas dataframe. 

```python 
def get_data(self, table, sql=None, *args, **kwargs):
```

**Arguments**:

* `table` (str): Name of the table to retrieve data from.
* `sql` (str): The optional SQL query to execute. Default value is None.

**Returns**

* `data` (dataframe): A Pandas dataframe object containing the data.

**Example Usage**

```python
from lolpop.component import DuckDBDataConnector

config = {
    #insert component config here
}

# create an instance of DuckDBDataConnector with default arguments
duck_conn = DuckDBDataConnector(conf=config)

# retrieve data from the database using an SQL select statement
df = duck_conn.get_data('your_table_name')
```

This example creates an instance of the DuckDBDataConnector class and uses the get_data() method to retrieve data from the database. 

### save_data

The `save_data` method saves data to the specified table in the specified DuckDBDataConnector instance. If the table does not exist, it gets created with the data structure from the dataframe provided. If a column is missing, it adds the column as nulls. This preserves the structure of the destination table.

```python 
def save_data(self, data, table, *args, **kwargs):
```

 **Arguments**

* `data` (pandas.DataFrame): Pandas dataframe containing the data to be saved.
* `table` (str): Name of the table to save the data to.

**Example Usage**

```python
from lolpop.component import DuckDBDataConnector 

config = {
    #insert component config here
}

# create an instance of DuckDBDataConnector with default arguments
duck_conn = DuckDBDataConnector(conf = config)

# create a Pandas dataframe object containing data
confluence_table = pd.DataFrame({
 'page': ['A', 'B', 'C'],
 'editorial': ['Ace', 'Bob', 'Chloe'],
 'when': ['2019-07-01', '2019-08-05', '2019-09-10']
})

# create table if it doesn't exist and save data to it
duck_conn.save_data(confluence_table, 'your_table_name')
```

This example creates an instance of the DuckDBDataConnector class, creates a Pandas dataframe and saves the content of the dataframe as a table in the database using the save_data() method.

### _load_data 

This method executes the given SQL command in DuckDB  and returns the retrieved data. 

```python 
_load_data(self, sql, path, *args, **kwargs)
```
**Arguments**:

- `sql`: (str) SQL command to execute.
- `path`: (str) Path to DuckDB instance.

**Returns**

- `pandas.DataFrame`: Fetched data from DuckDB.

### _save_data

```python 
_save_data(self, data, table_name, path, *args, **kwargs)
```

This method saves the given data to a table in DuckDB . 

 **Arguments**:

- `data`: (pandas.DataFrame) The data to save
- `table_name`: (str) Name of table to save data
- `path`: (str) Path to duckdb instance .

### __map_pandas_col_type_to_duckdb_type

This is a private method which maps pandas data types to duckdb data types.

```python 
def __map_pandas_col_type_to_duckdb_type(self, col_type):
```

**Arguments**:

* col_type (_type_): Pandas data type.

**Returns**

* column_type (_type_): DuckDB data type corresponding to pandas data type.
