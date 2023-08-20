The metaflow time series forecasting example is the same as the normal [time series forecasting](timeseries_forecasting.md) example. The only difference is that it users metaflow as the ML pipeline tool. You can follow the instructions in the [time series forecasting](timeseries_forecasting.md) example, with the following two modifications: 

1. When installing libraries for the example, be sure to install `lolpop[metaflow]` in addition to the other extras. 

2. When running the example you'll want to run it from the same directory, i.e. `lolpop_grocery_sales_example`, but run it via this command: 

```python
python3 metaflow/run.py 
```

The rest of it should look fairly identical. 

!!! Note 
    When using the metaflow pipelines, when you're logging to stdout, the logging will be be a bit redundant, as it currently applies both the metaflow and lolpop formats. In the future we may try to make this less noisy -- a quick fix if this annoys you is to modify the StdOutLogger class to just not include the redundant pieces. 