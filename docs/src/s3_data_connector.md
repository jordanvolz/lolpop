# S3DataConnector 

This class defines a data connector that reads from and writes to an AWS S3 bucket using the boto3 package. This class is a child of the BaseDataConnector class and inherits methods from this class.

## Configuration

### Required Configuration

- `AWS_S3_BUCKET`: S3 bucket name to read/write data to.
- `AWS_ACCESS_KEY_ID`: AWS access key id. 
- `AWS_SECRET_KEY_ID`: AWS secret key id. 
- `AWS_SESSION_TOKEN`: AWS session token. 

### Optional Configuration 

There is no optional configuration. 

### Default Configuration 
There is no default configuration. 

## Methods 
### get_data

This method reads data from an AWS S3 bucket and returns a Pandas DataFrame.

```python
def get_data(self, path, *args, **kwargs)
```

**Arguments**

- `path`: The location of the file in the bucket.

**Returns**
- A Pandas DataFrame containing the data from the bucket.

### save_data 

This method saves data into an AWS S3 bucket.

```python
def save_data(self, data, path, *args, **kwargs)
```

**Arguments**

- `data`: The data to be written into the bucket.
- `path`: The location of the file in the bucket.


### _load_data 
This method reads data from files within the AWS S3 bucket and returns a Pandas DataFrame.

```python
def _load_data(self, path, config, **kwargs)
```

**Arguments**

- `path`: The location of the file in the bucket.
- `config`: A dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

**Returns**
- A Pandas DataFrame containing the data from the file.

### _save_data
This method saves data into an AWS S3 bucket.

```python
def _save_data(self, data, path, config, *args, **kwargs)
```

**Arguments**
- `data`: The data to be written into the bucket.
- `path`: The location of the file in the bucket.
- `config`: A dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.


### _get_client
This method returns the AWS S3 client.

```python
def _get_client(self, config)
```

**Arguments**
- `config`: A dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

**Returns**
- An AWS S3 client.

## Usage


```python
from lolpop.component import S3DataConnector

config = {
    #insert component config here
}

s3 = S3DataConnector(conf=config)

data = s3.get_data('/path/to/data.csv')

new_data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})

s3.save_data(new_data, '/path/to/new_data.csv')
```