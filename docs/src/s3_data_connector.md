# S3DataConnector class documentation

This class defines a data connector that reads from and writes to an AWS S3 bucket using the boto3 package. This class is a child of the BaseDataConnector class and inherits methods from this class.

The S3DataConnector class includes the following methods:

### Constructor Method

```python
def __init__(self, *args, **kwargs)
```

This method is the constructor of the class. It loads the required configuration values for the S3 bucket from the specified `config` file.

### Get Data Method

```python
def get_data(self, path, *args, **kwargs)
```

This method reads data from an AWS S3 bucket and returns a Pandas DataFrame.

#### Parameters
- `path`: The location of the file in the bucket.

#### Returns
- A Pandas DataFrame containing the data from the bucket.

### Save Data Method

```python
def save_data(self, data, path, *args, **kwargs)
```

This method saves data into an AWS S3 bucket.

#### Parameters
- `data`: The data to be written into the bucket.
- `path`: The location of the file in the bucket.

#### Returns
- None

### Load Data Method

```python
def _load_data(self, path, config, **kwargs)
```

This method reads data from files within the AWS S3 bucket and returns a Pandas DataFrame.

#### Parameters
- `path`: The location of the file in the bucket.
- `config`: A dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

#### Returns
- A Pandas DataFrame containing the data from the file.

### Save Data Private Method

```python
def _save_data(self, data, path, config, *args, **kwargs)
```

This method saves data into an AWS S3 bucket.

#### Parameters
- `data`: The data to be written into the bucket.
- `path`: The location of the file in the bucket.
- `config`: A dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

#### Returns
- None

### Get Client Private Method

```python
def _get_client(self, config)
```

This method returns the AWS S3 client.

#### Parameters
- `config`: A dictionary that stores AWS S3 Buckets, AWS Access Key ID, AWS Secret Access Key, and AWS Session Token.

#### Returns
- An AWS S3 client.

### Examples

You can create an instance of the S3DataConnector class with the following code:

```python
import S3DataConnector

s3 = S3DataConnector()
```

You can fetch data from an S3 bucket with the following code:

```python
data = s3.get_data('data.csv')
```

You can save data to an S3 bucket with the following code:

```python
s3.save_data(data, 'data.csv')
```