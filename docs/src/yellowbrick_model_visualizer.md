## YellowbrickModelVisualizer 

The `YellowbrickModelVisualizer` class is a subclass of the `BaseModelVisualizer` class. It provides a set of methods for generating visualizations and saving plots for model evaluation. These visualizations can help users understand the performance of their machine learning models.


## Configuration 

### Required Configuration

The `YellowbrickModelVisualizer` class requires the following components: 

- `metadata_tracker`

and the following configuration:

- `local_dir`: A local directory to use to stage files before logging them to the `metadata_tracker`. 

## Optional Configuration 
The `YellowbrickModelVisualizer` class has no optional configuration. 

## Default Configuration 
The `YellowbrickModelVisualizer` class has no default configuration. 

### Methods

#### generate_viz

This method generates visualizations and saves plots for model evaluation.

```python 
def generate_viz(data, model, model_version, *args, **kwargs)
```

**Arguments:**

- `data`: A dictionary containing the training and testing data for the model evaluation.
- `model`: The trained model object for evaluation.
- `model_version`: The model version object from the `metadata_tracker` to save the visualizations to. 

**Returns:**

This method generates several visualization plots as side-effects. It does not return any values.

#### _save_plot 
This method fits and scores a visualization object and saves it to disk.

```python 
def _save_plot(viz, data, split, model_version, plot_name)
```

**Arguments:**

- `viz`: The Visualization object for plotting.
- `data`: A dictionary containing the training and testing data for the model evaluation.
- `split`: The string name of the sub-dataset we're plotting for.
- `model_version`: The model version object from the `metadata_tracker` to save the visualizations to. 
- `plot_name`: The name of the file to save the plot as.

**Returns:**

This method generates a single visualization plot as a side-effect. It does not return any values.

#### _save_pyplot 
This method saves a pyplot plot to disk.

```python 
def _save_pyplot(name, label, model_version)
```


**Arguments:**

- `name`: The name of the file to save the plot as.
- `label`: The string label for the sub-dataset we're plotting for.
- `model_version`: The model version object to save the plots to.

**Returns:**

- Returns a reference to the saved artifact.
- Saves a single plot as a side-effect.

## Usage

```python
from lolpop.component import YellowbrickModelVisualizer

.. #create data, model, and model_verison 

config = {
   #insert component configuration here
}

# Create an instance of the YellowbrickModelVisualizer class
visualizer = YellowbrickModelVisualizer(conf=config)

# Generate visualizations for model evaluation
visualizer.generate_viz(data, model, model_version)
```
