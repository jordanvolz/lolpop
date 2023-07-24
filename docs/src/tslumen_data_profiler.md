# tslumenDataProfiler

The `tslumenDataProfiler` class is a Python class that inherits from the `BaseDataProfiler` class. It is used to profile time series data using tslumen package. This class provides the `profile_data` method that profiles the data and returns the data report.

Note: The tslumen library is only meant to be used with time-series data. 

Note: The tslument library currently does not support data comparison. 

## Configuration

### Required Configuration
The tslumen data profiler requires the following configuration: 

- `local_dir`: Location of a local directory to output files generated by this component. 
- `time_index`: The time index of the data

### Optional Configuration
The tslumen data profiler uses the following  optional configuration: 

- `forecast_frequency`: The frequency of the data. Will be used if the frequency is unable to be inferred from the data. 


### Default Configuration
The tslumen data profiler uses the following optional configuration: 

  - `TSLUMEN_PROFILE_REPORT_NAME`: The name of the profile report file. Default is "TSLUMEN_DATA_PROFILE_REPORT.HTML".
 

## Methods

### profile_data

This method takes a pandas dataframe of the data to profile as a mandatory argument. It internally uses the `HtmlReport` function from the tslumen package to create a report of the data. It saves the report to a file in the path specified by the configuration parameter `TSLUMEN_PROFILE_REPORT_NAME` and returns the data report and file path as output.


```python
def profile_data(self, data, *args, **kwargs):
```

**Arguments**: 

- `data` (pd.DataFrame): A dataframe of the data to profile.  

**Returns**:
    
- `data_report` (object): Python object of the report 
- `file_path` (string): file path of the exported report
