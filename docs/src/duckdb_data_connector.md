# **DuckDBDataConnector Class Documentation**

This document explains the features of the DuckDBDataConnector class, which retrieves data from DuckDBDataConnector instance or custom SQL provided and saves data to the specified table in the specified instance. This class extends from the BaseDataConnector class.

## **Methods**
The class has four methods which have been documented in their respective sections below:

### **1. \_\_init\_\_() Method**

This is the constructor method for the DuckDBDataConnector class. It initializes the path attribute as self._get_config("duckdb_path").


#### Method Signature 
```python 
def __init__(self, *args, **kwargs):
```

#### Parameters:
*args and **kwargs (optional): represents the flexible arguments for the method.


### **2. get_data() Method**

The get_data() method retrieves data from the DuckDBDataConnector table or custom SQL provided and returns a Pandas dataframe. 

#### Method Signature 
```python 
def get_data(self, table, sql=None, *args, **kwargs):
```

#### Parameters:
*table (str): Name of the table to retrieve data from.
*sql (str): The optional SQL query to execute. Default value is None.
*args and **kwargs (optional): represents the flexible arguments for the method.

#### Returns
data (dataframe): A Pandas dataframe object containing the data.

#### Raises
Exception: If both table and sql statement are not provided.


#### Example Usage

```python
import DuckDBDataConnector

# create an instance of DuckDBDataConnector with default arguments
duck_conn = DuckDBDataConnector()

# retrieve data from the database using an SQL select statement
resulting_df = duck_conn.get_data('your_table_name')
```

This example creates an instance of the DuckDBDataConnector class and uses the get_data() method to retrieve data from the database. 

### **3. save_data() Method**

The save_data() method saves data to the specified table in the specified DuckDBDataConnector instance. If the table does not exist, it gets created with the data structure from the dataframe provided. If a column is missing, it adds the column as nulls. This preserves the structure of the destination table.

#### Method Signature 
```python 
def save_data(self, data, table, *args, **kwargs):
```

#### Parameters:
*data (pandas.DataFrame): Pandas dataframe containing the data to be saved.
*table (str): Name of the table to save the data to.
*args and **kwargs (optional): represents the flexible arguments for the method.

#### Returns
None

#### Raises
No exception is raised.

#### Example Usage

```python
# create an instance of DuckDBDataConnector with default arguments
duck_conn = DuckDBDataConnector()

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

### **4. \_map_pandas_col_type_to_duckdb_type() Method**

This is a private method which maps pandas data types to duckdb data types.

#### Method Signature 
```python 
def _map_pandas_col_type_to_duckdb_type(self, col_type):
```

#### Parameters:
*col_type (_type_): Pandas data type.

#### Returns
column_type (_type_): DuckDB data type corresponding to pandas data type.

#### Raises
No exception is raised.


#### Example Usage

This method is a private method and used inside the class, hence cannot be used on its own separately.

## **Dependencies**

The following packages need to be installed before using this class.

pandas, duckdb

```python 
!pip install pandas duckdb
```