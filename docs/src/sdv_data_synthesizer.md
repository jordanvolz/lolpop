# **Class SDVDataSynthesizer**
This class is a sub-class of `BaseDataSynthesizer` that operates in the Synthatic Data Vault (SDV) environment. It contains 5 methods to load, model, sample and evaluate synthetic data. 

## Methods

### load_data(self, source_file_path, file_type="csv", `*args`, `**kwargs`)
This method loads tabular data from a given file. It returns a pandas dataFrame of the data and metadata of the loaded data. 

**Arguments**:
 - `source_file_path`: String. Path to the file containing the data to be loaded
 - `file_type`: String. Type of file containing the data. Default is "csv".
 - `*args` and `**kwargs`: optional arguments and keyword arguments respectively for file loading.

**Returns**: 
Two objects; a pandas dataFrane of the loaded data and metadata of the data


### model_data(self, data, metadata, synthesizer_str=None, `*args`, `**kwargs`)
This method creates a synthesizer that is fit on given data using the sdv environment. The method returns a synthesizer model fit on the data.

**Arguments**: 
 - `data`: pandas dataframe of the input data
 - `metadata`: dictionary object representing metadata of the input data which should be the output of `load_data` method.
 - `synthesizer_str`: Optional string representing synthesizer to use. If not provided, a preset is used as default.
 - `*args` and `**kwargs`: optional arguments and keyword arguments respectively for synthesizer parameter. 

**Returns**:
The synthesizer object of the model fit on the input data. 

### sample_data(self, synthesizer, num_rows, `*args`, `**kwargs`)
This method samples generated data from an already created synthesizer object and returns a pandas dataframe of synthesized data.

**Arguments**:
 - `synthesizer`: synthesizer object obtained from the output of `model_data` function 
 - `num_rows`: integer. number of rows of data to generate.
 - `*args` and `**kwargs`: optional arguments and keyword arguments for synthesizer parameter. 

**Returns**:
An object of pandas dataframe as the generated synthetically data.

### evaluate_data(self, real_data, synthetic_data, metadata, synthesizer_str, `*args`, `**kwargs`)
This function returns reports on the quality of the synthetic data generated.

**Arguments**:
 - `real_data`: pandas dataframe of the original data
 - `synthetic_data`: pandas dataframe of the generated synthetic data
 - `metadata`: dictionary object obtained from the output of `load_data` method.
 - `synthesizer_str`: string representing the synthesizer. If not specified, it uses the default synthesizer.
 - `*args` and `**kwargs`: optional arguments and keyword arguments for synthesizer parameter. 

**Returns**: 
quality_report: report on the quality of the fake data obtained as an object
diagnostic_report: diagnostic results about the fake data obtained as an object


### `_get_synthesizer_class(self, synthesizer)`
This method returns a class object as specified by the synthesizer string. Private method used internally by the class.

**Arguments**: 
 - `synthesizer`: string representing the synthesizer class to be returned. 
 

### `_get_evaluator_class(self, synthesizer)`
This method returns an evaluator class object as specified by the synthesizer string. Private method used internally by the class.

**Arguments**: 
 - `synthesizer`: string representing the evaluator class to be returned. 
 

### `_get_diagnostic_class(self, synthesizer)`
This method returns a diagnostic class object as specified by the synthesizer. Private method used internally by the class.

**Arguments**: 
 - `synthesizer`: string representing the diagnostic class to be returned


## Usage Example
Below is an example of creating, modeling, and sampling synthetic data using `SDVDataSynthesizer`. 

```python
import sdv

SYNTHESIZER = "CopulaGAN"
sdv_synthesizer = sdv.SDVDataSynthesizer(SYNTHESIZER)

# load data
DATA_PATH = "./data/adult_data.csv"
data, metadata = sdv_synthesizer.load_data(DATA_PATH)

# fit the model
synthesizer = sdv_synthesizer.model_data(data, metadata, synthesizer_str=SYNTHESIZER)

# Generate synthetic data
num_rows= len(data)
syn_data = sdv_synthesizer.sample_data(synthesizer, num_rows)

# Evaluate synthetic data
quality_report, diagnostic_report = sdv_synthesizer.evaluate_data(data, syn_data, metadata, SYNTHESIZER)
```