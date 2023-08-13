A typical metaflow pipeline contains two classes, one class that inherits from the base `lolpop` class and one that inherits from the `metaflow` `FlowSpec` class (due to how `metaflow` handles inheritance we can't simply create a single class that inherits from multiple classes). The `FlowSpec` subclass is where you will put your standard `metaflow` pipeline definition. The `lolpop` subclass will typically be very similar across implementations. This class contains two main methods: `run`, which runs the `metaflow` `FlowSpec` class, and `get_artifacts`, which retrieves artifacts from `metaflow` and surfaces them back to the `lolpop` runner. 

The main different thing that you should do in the `FlowSpec` subclass is register your `lolpop` objects in the `__init__` class, where `self.lolpop` will be the `lolpop` pipeline subclass. Then in your `metaflow` class you'll be able to access any normal `lolpop` resources via `self.lolpop.<X>`. 

See one of the [built-in components](https://github.com/jordanvolz/lolpop/blob/main/lolpop/pipeline/process/metaflow_offline_process.py) for an example of working with Metaflow. 