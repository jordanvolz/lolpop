# Class Documentation: tslumenDataProfiler

The `tslumenDataProfiler` class is a Python class that inherits from the `BaseDataProfiler` class. It is used to profile time series data using tslumen package. This class provides the `profile_data` method that profiles the data and returns the data report.

## Class Methods

### profile_data

```python
def profile_data(self, data, *args, **kwargs):
    """Profiles data using tslumen

    Args:
        data (pd.DataFrame): A dataframe of the data to profile.  

    Returns:
        data_report (object): Python object of the report 
        file_path (string): file path of the exported report

    """
```

This method takes a pandas dataframe of the data to profile as a mandatory argument. It internally uses the `HtmlReport` function from the tslumen package to create a report of the data. It saves the report to a file in the path specified by the configuration parameter `TSLUMEN_PROFILE_REPORT_NAME` and returns the data report and file path as output.

## Configuration

### __REQUIRED_CONF__

```python
__REQUIRED_CONF__ = {
    "config": ["local_dir"]
}
```

This is a dictionary that holds configuration parameters required by the class. It contains the key `config` which is associated with a list of configuration parameters. In this case, we have only one required configuration parameter named `local_dir`, which specifies the local directory where the data report will be saved.

### __DEFAULT_CONF__

```python
__DEFAULT_CONF__ = {
    "config": {"TSLUMEN_PROFILE_REPORT_NAME": "TSLUMEN_DATA_PROFILE_REPORT.HTML"}
}
```

This dictionary holds the default configuration parameters for the class. It contains the key `config` associated with a dictionary of configuration parameters. In this case, the default configuration specifies the name of the data report file that will be created as `TSLUMEN_DATA_PROFILE_REPORT.HTML`.