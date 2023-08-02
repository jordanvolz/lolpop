
## Overview

A `test_recorder` is a component that is able to track and manage tests that are run via lolpop's [testing framework](testing_workflows.md). The intention is to collect tests results via a `test_recorder` and then print off a report at the completion of the test. 

## Attributes

`BaseTestRecorder` contains no default attributes: 

## Configuration

`BaseTestRecorder` contains no default or required configuration. 


## Interface

The following methods are part of `BaseTestRecorder` and should be implemented in any class that inherits from this base class: 

### record_test

Record the results of a test. 

```python
def record_test(self, obj, method, test, test_method, result, msg, *args, **kwargs)
```

**Arguments**: 

- `obj` (object): The lolpop object that was tested
- `func` (object): The method of the object that was tested.
- `test` (object): The test module used.
- `test_method` (object): The method in the test file that was run. 
- `result` (bool): The test Result (`True` = "passed"). 
- `msg` (str): Additional message sent from the test. 

### print_report

Prints a test report.  This is meant for interactive use, such as running tests from the CLI. 

```python
def print_report(*args, **kwargs)
```

**Arguments**: 

None


### generate_report 

Similar to print_report, but generates a physical report. Intended to be used for non-interactive teseting use (i.e. automated testing). 

```python
def generate_report(*args, **kwargs)
```

**Arguments**: 

None

