# Technical Documentation for `StdOutLogger` Python Class

The `StdOutLogger` class is a Python class that provides a standard output log for logging messages to the console. This class is a child class of the `BaseLogger` class, which is a base class for all logger classes in this implementation.

## `__DEFAULT_CONF__` Property

This property is a dictionary that provides the default configuration for the `StdOutLogger` class. This dictionary contains `log_level` and `use_line_numbers` key-value pairs.

- `log_level`: This key-value pair specifies the default logging level for `StdOutLogger`. The possible values are `NONE`, `FATAL`, `ERROR`, `WARN/WARNING`, `INFO`, `DEBUG`, `TRACE`, and `ALL`. The default value is `DEBUG`.
- `use_line_numbers`: This boolean key-value pair specifies if the line numbers should be displayed in the log message or not. The default value is `False`.

## `__init__` Method

This method is the constructor for the `StdOutLogger` class. It initializes the logger with the `super().__init__()` method and initializes the colorama module for colored output.

## `log` Method

This method logs the message to the standard output. The method takes six mandatory arguments and two optional arguments as follows:

- `msg` (str): The message to be logged.
- `level` (str): The level of logging for the message.
- `time` (str, optional): The timestamp for the message (default=None).
- `process_name` (str, optional): The name of the process (default=None).
- `line_num` (int, optional): The line number of the message (default=None).
- `*args`: Variable length argument list.
- `**kwargs`: Arbitrary keyword arguments.

If the logging level of the message is lower than or equal to the set logging level of the logger, then the method generates the log message based on the configuration of the logger such as the timestamp, name of the process, and line number. It then prints the log message to the standard output.

The method does not return any value.

## `_get_level_value` Method

This method takes a logging level in the form of a string and returns the corresponding numeric logging level value for that string. The method returns the following numeric values based on the given string input:

- `NONE`: `0`
- `FATAL`: `1`
- `ERROR`: `2`
- `WARN/WARNING`: `3`
- `INFO`: `4`
- `DEBUG`: `5`
- `TRACE`: `6`
- `ALL`: `100`

The method does not raise any exception.

## `_get_level_format` Method

This method takes a logging level and returns the formatted level with color codes based on the level of severity. The method uses the `colorama` module to add color codes to the output.

The method returns the formatted level as a string.

## Example Usage

```
import logging

console_handler = logging.StreamHandler()
logger = StdOutLogger(name="mylogger")

logger.addHandler(console_handler)
logger.setLevel("DEBUG")

logger.log("Debugging", level="DEBUG", process_name="myprocess")
```

In this example, we import the `logging` module, create a `StreamHandler` object that redirects the logs to the console, and create an instance of the `StdOutLogger` class named `mylogger`.

We then add the `console_handler` to our logger and set the logging level to `DEBUG`. Finally, we log a message using the `log` method with a message, logging level, and process name.