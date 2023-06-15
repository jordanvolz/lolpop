```
@class YellowbrickModelVisualizer(BaseModelVisualizer):
```

This class contains visualizations related to model evaluation using the Yellowbrick library.

```
def generate_viz(self, data, model, model_version):
```

Generate visualizations and save plots for model evaluation.

Args:
- `data`: A dictionary containing the training and testing data for the model evaluation.
- `model`: The trained model object for evaluation.
- `model_version`: The version string for the model being evaluated.

Returns:
- Generates several visualization plots as side-effects.
- No return values.

```
def _save_plot(self, viz, data, split, model_version, plot_name):
```

Fit and score a visualization object and save it to disk.

Args:
- `viz`: The Visualization object for plotting.
- `data`: A dictionary containing the training and testing data for the model evaluation.
- `split`: The string name of the sub-dataset we're plotting for.
- `model_version`: The version string for the model being evaluated.
- `plot_name`: The name of the file to save the plot as.

Returns:
- Generates a single visualization plot as a side-effect.
- No return values.

```
def _save_pyplot(self, name, label, model_version):
```

Save a pyplot plot to disk.

Args:
- `name`: The name of the file to save the plot as.
- `label`: The string label for sub-dataset we're plotting for.
- `model_version`: The version string for the model being evaluated.

Returns:
- Returns a reference to the saved artifact.
- Saves a single plot as a side-effect.