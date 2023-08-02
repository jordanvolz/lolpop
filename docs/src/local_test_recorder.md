# LocalTestRecorder

The `LocalTestRecorder` class is a subclass of the `BaseTestRecorder` class. It is used to record and print test results in a local testing environment. This class provides two methods: `record_test` and `print_report`.

## Attributes

`LocalTestRecorder` contains the following attributes: 

- `test_results`: A list of test results. Each test result should be a dictionary which describes the test and its result. 

## Configuration 

## Methods

### record_test
This method is used to record the results of a test.

```python
def record_test(self, obj, method, test, test_method, result, msg=None, *args, **kwargs):
    pass
```

**Arguments**: 

- `obj` (object): The lolpop integration being tested.
- `method` (object): The method in the integration being tested.
- `test` (object): The test module used.
- `test_method` (object): The method in the test module used.
- `result` (bool): The result of the test. True indicates the test passed, and False indicates the test failed.
- `msg` (str, optional): Additional information returned from the test. Defaults to None.

### print_report
This method prints a testing report based on the recorded test results.

```python
def print_report(self):
    pass
```



## Usage

This is intended only to be used within the [lopop testing framework](testing_workflows.md) and with the [lolpop cli](cli.md). 