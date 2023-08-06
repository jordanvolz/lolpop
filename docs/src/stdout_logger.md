# StdOutLogger

The `StdOutLogger` class is a Python class that provides a standard output log for logging messages to the console. This class is a child class of the `BaseLogger` class, which is a base class for all logger classes in this implementation. `StdOutLogger` is primarily designed to be used in development workflows. 


## Configuration

### Required Configuration
`StdOutLogger` contains no required configuration.

### Optional Configuration
`StdOutLogger` has no optional configuration.

### Default Configuration

`StdOutLogger` has no default configuration. 

## Methods 

### log

This method logs the message to the standard output. If the logging level of the message is lower than or equal to the set logging level of the logger, then the method generates the log message based on the configuration of the logger such as the timestamp, name of the process, and line number. It then prints the log message to the standard output.

```python 
def log(self, msg, level, time=None, process_name=None, line_num=None, *args, **kwargs)
```

**Arguments**:

- `msg` (str): The message to be logged.
- `level` (str): The level of logging for the message.
- `time` (str, optional): The timestamp for the message (default=None).
- `process_name` (str, optional): The name of the process (default=None).
- `line_num` (int, optional): The line number of the message (default=None).


**Example**:
```python
from lolpop.components import StdOutLogger

config = {
    #insert component config here 
}

logger = StdOutLogger(conf=config)

# Log a message with the level "INFO"
logger.log("Sample log message", "INFO")

# Log an error message with specific time and process name
logger.log("Error message", "ERROR", time=datetime.utcnow(), process_name="my_app_name")
```


### _get_level_value 
This method takes a logging level in the form of a string and returns the corresponding numeric logging level value for that string. The method returns the following numeric values based on the given string input:

- `NONE`: `0`
- `FATAL`: `1`
- `ERROR`: `2`
- `WARN/WARNING`: `3`
- `INFO`: `4`
- `DEBUG`: `5`
- `TRACE`: `6`
- `ALL`: `100`


```python
def _get_level_value(self, level)
```

**Arguments**: 

- level: The string log level value. 

**Returns**: 

The numeric value of the log level.


## _get_level_format

This method takes a logging level and returns the formatted level with color codes based on the level of severity. The method uses the `colorama` module to add color codes to the output.

```python
def _get_level_format(self, level)
```
**Arguments**: 

- level: The string log level value. 

**Returns**: 

The method returns the formatted level as a string.
