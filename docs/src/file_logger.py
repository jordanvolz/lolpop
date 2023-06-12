# FileLogger Class

The `FileLogger` class is a subclass of `BaseLogger` that provides logging functionality to write logs to a file. This class extends the functionality of the `BaseLogger` class by adding a filename and allowing the user to specify the level of logging, process name, line numbers, and time.

## Usage
To use the `FileLogger` class in your Python application, first import it using `from <module_name> import FileLogger`. Then create an instance of the class by calling `FileLogger()` with any necessary arguments.

```python
from logging_module import FileLogger

# Create a new instance of the FileLogger class
logger = FileLogger()
```

## FileLogger Class Methods

### __init__(self, *args, **kwargs)

The `__init__` method initializes a new `FileLogger` object, with an optional filename and logging level. By default, it creates a log file with a filename of 'lolpop.log', and the logging level is set to 'INFO'.

#### Parameters
*args: Variable length argument list.<br>
**kwargs: Arbitrary keyword arguments.

#### Example:
```python
# Create a new instance of the FileLogger class with filename 'myapp.log' and logging level 'DEBUG'
logger = FileLogger(log_filename="myapp.log", log_level="DEBUG")
```

### log(self, msg, level, time = None, process_name=None, line_num=None, *args, **kwargs)

The `log` method logs a message with the specified logging level, time, process name, and line number. If the logging level is higher than or equal to the value specified in the configuration file, the message is logged. The method also includes additional information such as process name, line number, and time stamps.

#### Parameters
* `msg` (str): Message to be logged.
* `level` (str): Logging level to use.
* `time` (datetime, optional): Time to use. Defaults to None.
* `process_name` (str, optional): Name of the process. Defaults to None.
* `line_num` (int, optional): Line number associated with message. Defaults to None.
* `*args`: Variable length argument list.<br>
* `**kwargs`: Arbitrary keyword arguments.

#### Example:
```python
# Log a message with the level "INFO"
logger.log("Sample log message", "INFO")

# Log an error message with specific time and process name
logger.log("Error message", "ERROR", time=datetime.utcnow(), process_name="my_app_name")
```

### _get_level_value(self, level)

The `_get_level_value` method returns a numeric logging level value associated with the specified string level value. 

#### Parameters
* `level` (str): The string logging level value.

#### Returns
* The corresponding numeric logging level value.

#### Raises 
None.

#### Example:
```python
# Get the numeric logging level value associated with the string level "WARN"
value = logger._get_level_value("WARN")
print(value) # Output: 3
```