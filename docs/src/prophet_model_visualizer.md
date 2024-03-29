# ProphetModelVisualizer

The `ProphetModelVisualizer` class is a subclass of the `BaseModelVisualizer` class and provides methods for generating visualizations of Prophet model components and forecasts, as well as performing time-series cross validation on the Prophet model.


## Configuration 

### Required Configuration

The `ProphetModelVisualizer` class requires the following components: 

- `metadata_tracker`

and the following configuration:

- `local_dir`: A local directory to use to stage files before logging them to the `metadata_tracker`. 

## Optional Configuration 
The `ProphetModelVisualizer` class has no optional configuration. 

## Default Configuration 
The `ProphetModelVisualizer` class has no default configuration. 

## Methods

### generate_viz 
Method to generate visualizations of Prophet model components and forecasts.

```python
def generate_viz(self, data, model, model_version, forecast_period=7, forecast_frequency="D", *args, **kwargs)
```

**Arguments**:

- `data`: (pandas.DataFrame) Input DataFrame containing time-series data.
- `model`: (Prophet model object) A trained Prophet model object.
- `model_version`: (object) Model version from the `metadata_tracker`.
- `forecast_period`: (int, default 7) The period for which forecast is to be generated.
- `forecast_frequency`: (str, default 'D') The frequency of the forecast period.



### cross_validation 
Method to perform time-series cross validation on the Prophet model.

```python 
def cross_validation(self, model, model_version, initial, period, horizon, *args, **kwargs)
```

**Arguments**:

- `model`: (Prophet model object) A trained Prophet model object.
- `model_version`: (str) String defining the model version.
- `initial`: (str, int or float) String or numerical value to define the size of the initial training period.
- `period`: (str, int or float) String or numerical value to define the length of the spacing between cutoff dates.
- `horizon`: (str, int or float) String or numerical value to define the forecast horizon.

### _save_and_log_file 
Helper method to save plots generated by ProphetModelVisualizer methods to a local directory and log them with the metadata tracker.

```python 
def _save_and_log_file(self, dir, id, file_name, model_version)
```

**Arguments**:

- `dir`: (str) Directory path for saving the file.
- `id`: (str) Unique identifier for the model version.
- `file_name`: (str) Name for the file to be saved.
- `model_version`: (object) Model version to log the file to.


## Usage:

```python
from lolpop.component import ProphetModelVisualizer

... #create data, model, model_version 

config = {
    #insert component config here
}

visualizer = ProphetModelVisualizer(conf=config)

# Generate visualizations
visualizer.generate_viz(data, model, model_version, forecast_period=7, forecast_frequency='D')

# Perform cross validation
visualizer.cross_validation(model, model_version, initial='730 days', period='180 days', horizon='365 days')
```