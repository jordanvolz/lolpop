# FileLogger

The `FileLogger` class is a subclass of `BaseLogger` that provides logging functionality to write logs to a file. This class extends the functionality of the `BaseLogger` class by adding a filename and allowing the user to specify the level of logging, process name, line numbers, and time.

## Configuration

### Required Configuration
`FileLogger` contains no required configuration.

### Optional Configuration
`FileLogger` has no optional configuration.

### Default Configuration

`FileLogger` contains the following default configuration: 

- `log_filename`: The file to log output to. Defaults to `lolpop.log`
- `log_level`: The logging level. Defaults to `DEBUG`
- `log_format`: The logging format to use. Defaults to "%(message)s"
- `use_line_numbers`: Whether or not to include line numbers in the logging output. Defaults to `False`


## Methods 

### log 
The `log` method logs a message with the specified logging level, time, process name, and line number. If the logging level is higher than or equal to the value specified in the configuration file, the message is logged. The method also includes additional information such as process name, line number, and time stamps.

```python 
def log(self, msg, level, time = None, process_name=None, line_num=None, *args, **kwargs)
```


**Arguments**

* `msg` (str): Message to be logged.
* `level` (str): Logging level to use.
* `time` (datetime, optional): Time to use. Defaults to None.
* `process_name` (str, optional): Name of the process. Defaults to None.
* `line_num` (int, optional): Line number associated with message. Defaults to None.

**Example**:
```python
from lolpop.components import FileLogger

config = {
    #insert component config here 
}

logger = FileLogger(conf=config)

# Log a message with the level "INFO"
logger.log("Sample log message", "INFO")

# Log an error message with specific time and process name
logger.log("Error message", "ERROR", time=datetime.utcnow(), process_name="my_app_name")
```

### _get_level_value 
The `_get_level_value` method returns a numeric logging level value associated with the specified string level value. 

```python 
_get_level_value(self, level)
```


**Arguments**
* `level` (str): The string logging level value.

**Returns**
* The corresponding numeric logging level value.
