## Overview

A `data_synthesizer` is a component that is able to synthesizer a dataset given a sample dataset. The intention it to allow building of datasets of arbitrarily large size given a representative sample. 

## Attributes

`BaseDataSynthesizer` contains no default attributes. 

## Configuration

`BaseDataSynthesizer` contains no default or required configuration. 


## Interface

The following methods are part of `BaseDataSynthesizer` and should be implemented in any class that inherits from this base class: 

### spit_data

Performs a data split on the given data. 

```python
def load_data(self, source_file, *args, **kwargs) -> tupe[Any, Any]
```

**Arguments**: 

- `source_file` (object): File location of the source data to use as a sample for synthesis.   

**Returns**:

- `data` (object): An object representing the loaded data. Very like a pandas.DataFrame.  
- `metadata` (Any): A python object containing metadata about the loaded data. 

### model_data

Creates a model for synthesizing data given a sample.  

```python
def model_data(self, data, *args, **kwargs) -> Any
```

**Arguments**: 

- `data` (object): Data to model.   

**Returns**:

- `model` (Any): A model that can synthesize new data. 

### sample_data

Generates new sample data given a synthetic model.  

```python
def sample_data(self, model, num_rows, *args, **kwargs) -> Any
```

**Arguments**: 

- `model` (object): The synthetic model to use. 
- `num_rows`  (int): The number of rows to generate. 

**Returns**:

- `data` (object): The generated data. Most likely a `pandas.DataFrame`, or similar. 

### evaluate_data

Evaluates synthetic data given a sample of real data.   

```python
def evaluate_data(self, real_data, synthetic_data, *args, **kwargs) -> list[Any]:
```

**Arguments**: 

- `real_data` (object): Real data from the original dataset.  
- `synthetic_data`  (object): A sample of synthetic data, likely generated from `sample_data`. 

**Returns**:

- `list` (object): A list of reports generated to evaluate the model. 

