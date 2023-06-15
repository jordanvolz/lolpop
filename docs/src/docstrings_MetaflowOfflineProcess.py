```
Class MetaflowOfflineProcess(BaseProcess):
    """
    A class for executing offline Metaflow flows.

    Attributes:
        __REQUIRED_CONF__ (dict): A dictionary defining required configurations.
            components (list): A list of components required for the flow to execute.
            config (list): A list of configurations required for the flow to execute.
    """

    __REQUIRED_CONF__ = {
        "components": ["data_transformer", "metadata_tracker", "resource_version_control", "data_profiler", "data_checker"],
        "config": []
    }

    @utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
    def run(self, source_data_name, source_data, **kwargs):
        """
        Execute the offline Metaflow flow.

        Args:
            source_data_name (str): The name of the data source.
            source_data (object): The object containing the source data.
            **kwargs: Any additional arguments to pass to the flow.

        Returns:
            None.

        Raises:
            Any exceptions raised during Metaflow execution.
        """

        # get flow class object from this file
        mod_cl = meta_utils.get_flow_class(__file__, METAFLOW_CLASS)

        flow = meta_utils.load_flow(mod_cl, self, PLUGIN_PATHS, source_data=source_data, source_data_name=source_data_name)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)

        meta_utils.run_flow(flow, "run", __file__, PLUGIN_PATHS)
        self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)

    def get_artifacts(self, artifact_keys):
        """
        Retrieve artifacts from the latest run of the pipeline.

        Args:
            artifact_keys (list): A list of artifact keys to retrieve.

        Returns:
            artifacts (dict): A dictionary containing the requested artifacts.

        Raises:
            Any exception raised during the retrieval of artifacts from the run.
        """

        # get latest run of this pipeline
        run = meta_utils.get_latest_run(METAFLOW_CLASS)

        # get requested artifacts
        artifacts = meta_utils.get_run_artifacts(run, artifact_keys, METAFLOW_CLASS)

        return artifacts
```

In the above code, `MetaflowOfflineProcess` is a Python class for running offline Metaflow flows. The class has two methods: `run` and `get_artifacts`.

`run` method loads and executes the Metaflow flow. The method takes `source_data_name` and `source_data` as inputs along with any other keyword arguments. `source_data_name` is a string that identifies the name of the data source and `source_data` is an object that contains the data. The method returns `None`. It raises an exception if there is any error during the Metaflow execution.

`get_artifacts` method retrieves artifacts from the latest run of the pipeline. The method takes a list of `artifact_keys` as input and returns a dictionary containing the requested artifacts. The method raises an exception if there is any error during the retrieval of artifacts.