# StdOutNotifier

The `StdOutNotifier` class is a subclass of the `BaseNotifier` class. It provides a method to print error messages to the standard output. 


## Configuration 

### Required Configuration
`StdOutNotifier` contains no required configuration.

### Optional Configuration
`StdOutNotifier` has no optional configuration.

### Default Configuration

`StdOutNotifier` has no default configuration.

## Methods 

### notify
The `notify` method is used to print an error message to the standard output.

```python
def notify(self, msg, level="ERROR", *args, **kwargs):
```

**Arguments**: 

- `msg` (str): The message to be printed to the standard output.
- `level` (str): The level of the message. This parameter is optional and defaults to "ERROR".


### Usage:

```python
from lolpop.component import StdOutNotifier

config = {
    #insert component config
}

notifier = StdOutNotifier(conf=config)
notifier.notify("An error occurred!", level="ERROR")
```

