## Overview

A `notifier` is a component that is able to send notification externally to the lolpop system. This allows lolpop to send notifications about system failures or results that fall outside of an accepted threshold, etc.   


## Attributes

`BaseNotifier` contains no default attributes. 

## Configuration

`BaseNotifier` contains no default or required configuration. 


## Interface

The following methods are part of `BaseNotifier` and should be implemented in any class that inherits from this base class: 

### notify

Sends a notification to an external system.   

```python
def notify(self, msg, level, *args, **kwargs)
```

**Arguments**: 

- `msg` (str): The notification message.   
- `level` (str): The notification level. 

