```
class MetaflowOfflineDeploy(BaseDeploy):
    """
    A class for deploying MetaflowOfflineDeploy.

    Attributes:
    -----------
        BaseDeploy : class
            A base class for deployment.
    """

    def run(self, model, model_version, **kwargs):
        """
        Runs the MetaflowOfflineDeploy.

        This method loads a Metaflow flow object based on the current file, loads the flow, 
        and then runs it using the model and version provided. This method logs execution 
        and returns nothing. 

        Parameters:
        -----------
            model : str
                The name of the model to run.
            model_version : str
                The version of the model to run.
            **kwargs : dict
                Other, non-specified parameters 

        Returns:
        --------

        Raises:
        -------
        """
        
        mod_cl = meta_utils.get_flow_class(__file__, METAFLOW_CLASS)

        flow = meta_utils.load_flow(
            mod_cl, self, PLUGIN_PATHS, model=model, model_version=model_version)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)

        meta_utils.run_flow(flow, "run", __file__, PLUGIN_PATHS)
        self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)

    def get_artifacts(self, artifact_keys):
        """
        Obtains artifacts of the MetaflowOfflineDeploy.

        This method gets the latest run of the MetaflowOfflineDeploy pipeline and returns the 
        requested artifacts. 

        Parameters:
        -----------
            artifact_keys : list
                A list of keys for the artifacts being requested. 

        Returns:
        --------
            artifacts : dict
                A dictionary of requested artifacts.
        
        Raises:
        -------
        """

        run = meta_utils.get_latest_run(METAFLOW_CLASS)

        artifacts = meta_utils.get_run_artifacts(
            run, artifact_keys, METAFLOW_CLASS)

        return artifacts
```