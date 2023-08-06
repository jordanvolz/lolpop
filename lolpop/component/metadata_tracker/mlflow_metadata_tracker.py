from lolpop.component.metadata_tracker.base_metadata_tracker import BaseMetadataTracker
from lolpop.utils import common_utils as utils
from lolpop.utils import mlflow_utils
#import your libraries here
import mlflow
from mlflow.tracking import MlflowClient as client
from pathlib import Path



@utils.decorate_all_methods([utils.error_handler, 
                             utils.log_execution(), 
                             mlflow_utils.check_active_mlflow_run(mlflow)])
class MLFlowMetadataTracker(BaseMetadataTracker):
    #Override required or default configurations here for your class
    ##Add required configuration here
    __REQUIRED_CONF__ = {
        "config": ["mlflow_tracking_uri", "mlflow_experiment_name"]
    }
    ##Add default configuration here
    #__DEFAULT_CONF__ = {
    #    "config": {}
    #}

    def __init__(self, *args, **kwargs):
        #set normal config
        super().__init__(*args, **kwargs)

        tracking_uri = self._get_config("mlflow_tracking_uri")
        experiment_name = self._get_config("mlflow_experiment_name")

        self.client, self.run = mlflow_utils.connect(tracking_uri, experiment_name)
        self.url = tracking_uri

        self.log("Using MLFlow in experiment %s with run id: %s" %(experiment_name, self.run.info.run_id), level="INFO")

    def log_artifact(self, resource, id, path, *args, **kwargs):
        """Saves artifact path to the artifact directory in the MLflow run specified in the resource.
        Inputs:
            resource: a tuple containing resource id and run.
            id: string representing the artifact ID.
            path: path to the artifact that needs to be saved.
        Outputs: None
        """
        run = resource[1]
        run_id = run.info.run_id
        resource_id = self.get_resource_id(resource)
        self.client.log_artifact(run_id, path, artifact_path=resource_id)
        self.log("Saving artifact %s to directory %s in artifact directory in run %s" %(path, id, run_id))

    def get_artifact(self, resource, id, *args, **kwargs):
        pass

    def log_tag(self, resource, key, value, *args, **kwargs):
        """Sets the tag with key and value for the MLflow run specified in the resource.
        Inputs:
            resource: tuple containing resource id and run.
            key: string tag key.
            value: string tag value.
        Outputs: None
        """
        run = resource[1]
        run_id = run.info.run_id
        resource_id = self.get_resource_id(resource)
        key = "%s.%s" % (resource_id, key)
        self.log("Saving tag key=%s, value=%s to run %s" %(key, value, run_id))
        self.client.set_tag(run_id, key, value)

    def get_tag(self, resource, key, *args, **kwargs):
        """Returns the value of the tag with key for the MLflow run specified in the resource.
        Inputs:
            resource: tuple containing resource id and run.
            key: string tag key.
        Outputs: The value of the tag with key for the MLflow run specified in the resource.
        """
        run = mlflow_utils.get_run(self.client, resource[1].info.run_id)
        resource_id = self.get_resource_id(resource)
        key = "%s.%s" % (resource_id, key)
        return run.data.tags.get(key)


    def log_metadata(self, resource, id, data, *args, **kwargs):
        """Saves metadata key=value to the MLflow run specified in the resource.
        Inputs:
            resource: tuple containing resource id and run.
            id: string metadata ID.
            data: metadata to store.
        Outputs: None
        """
        run = resource[1]
        run_id = run.info.run_id
        self.log("Saving metadata key=%s, value=%s to run %s" %
                 (id, str(data), run_id))
        #special handling for params, although we still want to save as a tag for retrieval purposes later on
        if "param" in id: 
            for k,v in data.items(): 
                self.client.log_param(run_id, k, v)
        self.log_tag(resource, id, data)


    def get_metadata(self, resource, id, *args, **kwargs):
        """Returns the metadata value with ID for the MLflow run specified in the resource.
        Inputs:
            resource: tuple containing resource id and run.
            id: string metadata ID.
        Outputs: The metadata value with ID.
        """
        value = self.get_tag(resource, id)
        return value

    # id + run_id unique identifies resource
    def create_resource(self, id, type=None, parent=None, *args, **kwargs):
        """Method to create a new MLflow run or nested run.
        Inputs:
            id: string ID of the resource.
            type: string with the value "experiment" or None.
            parent: tuple containing the parent resource id and run or None.
        Outputs: tuple containing the new resource ID and run.
        """
        if type == "experiment": 
            parent_id = self.get_resource_id(parent)
            parent_run = parent[1]
            run = mlflow_utils.create_nested_run(parent_run)
            self.log("Created nested run with id %s under parent %s." %(run.info.run_id, parent_run.info.run_id))
            id = "%s.%s" %(run.info.run_id, parent_id)
        else:
            run = self.run
        return (id, run)

    def get_resource(self, id, type, parent=None, *args, **kwargs):
        """Given a resource id and a type, returns tuple containing the resource id and run.
        Inputs:
            id: string ID of the resource to retrieve.
            type: string with the value "experiment" or None.
            parent: tuple containing the parent resource id and run or None.
        Outputs: tuple containing the resource ID and run.
        """
        run = self.run 
        if type=="experiment": 
            run_id, _ = id.split(".")
            run = self.client.get_run(run_id=run_id)
        else: 
            if parent is not None: 
                run = parent[1]
        return (id, run)

    #can't update runInfo properties like start_time/end_time
    def update_resource(self, resource, updates, *args, **kwargs):
        pass

    def clean_resource(self, resource, type, *args, **kwargs):
        """Ends MLflow run described in the resource.
        Inputs:
            resource: tuple containing resource id and run.
            type: string "experiment" or None.
        Outputs: None
        """
        if type=="experiment": 
            #end the nested run, this will make the parent run active again
            mlflow.end_run()

    def get_prev_resource_version(self, resource, extra_filters=[], num=1, *args, **kwargs):
        """Returns the previous resource version for the specified resource and any additional filters. 
        Inputs:
            resource: tuple containing resource ID and run.
            extra_filters: list of extra filters to be applied as strings.
                Example: ["tags.tag_key='tag_value'".
            num: int number of records to return.  
        Outputs: tuple containing the resource ID and run of the previous resource version.
        """
        run = resource[1]
        id = self.get_resource_id(resource)
        filter_string = ""
        for filter in extra_filters: 
            filter_string = "%s and %s" %(filter_string,filter)
        run_list = self.client.search_runs(
                        experiment_ids=run.info.experiment_id,
                        filter_string="attributes.start_time <= %s and attribute.status = 'FINISHED' and tags.parent_run = 'True' and tags.%s.exists = 'True'%s" %(run.info.start_time, id, filter_string), 
                        order_by=["attributes.start_time DESC"],
                        max_results=num,
                        )
        if len(run_list) > 0: 
            if num == 1:    
                return (resource[0], run_list[0])
            else: 
                return (resource[0], run_list)
        else: 
            return None

    #technically we should probably get model from the model repository, but I don't like metadata_tracker knowing about other components
    def get_currently_deployed_model_version(self, model_version, *args, **kwargs):
        """Returns the deployed version of the provided model version, if any.
        Inputs:
            model_version: tuple containing model version ID and run.  
        Outputs: tuple containing ID and run object of the deployed model version.
        """
        id = self.get_resource_id(model_version)
        deployed_mv = self.get_prev_resource_version(model_version, extra_filters=["tags.%s.status = 'DEPLOYED'" %id])
        #if no deployed model, just get the latest promoted model
        if deployed_mv is None: 
            deployed_mv = self.get_prev_resource_version(
                model_version, extra_filters=["tags.%s.status = 'PROMOTED'" % id])
        #if no deployed model, just get the previous model version 
        if deployed_mv is None: 
            deployed_mv = deployed_mv = self.get_prev_resource_version(model_version)
        return deployed_mv

    def get_prediction_job_model_version(self, prediction_job, *args, **kwargs):
        """Given a prediction_job identifier, returns the run and ID for the associated model version.
        Inputs:
            prediction_job: tuple containing prediction job ID and run or string that represents a prediction job.
        Outputs: tuple containing the model version ID and run.
        """
        run = prediction_job[1]
        id = prediction_job[0]
        if "_predictions" in prediction_job:
            id = id[:-12] 

        return (id, run)

    def get_latest_model_resource(self, model, type, *args, **kwargs):
        """If type is 'prediction_job,' will return the latest model verison.
        Inputs:
            model: tuple containing model ID and run.
            type: string "prediction_job" or other.
        Outputs: model version
        """
        if type == "prediction_job": 
            id = self.get_resource_id(model)
            prediction_id = id + "_predictions"
            prev_run = self.get_prev_resource_version(model, extra_filters=["tags.%s.exists = 'True'" %prediction_id])
            return (prediction_id, prev_run)
        else: 
            pass 

    def get_winning_experiment(self, model_version, *args, **kwargs):
        """Returns the ID and run of the experiment that produced the winning model for the provided model version.
        Inputs:
            model_version: tuple containing model version ID and run.
        Outputs: tuple
        """
        winning_experiment_id = self.get_tag(model_version, "winning_experiment_id")
        experiment = self.get_resource(winning_experiment_id, type="experiment", parent=model_version)
        return experiment

    def build_model_lineage(self, model_version, dataset_versions, *args, **kwargs):
        """Logs dataset versions used to create the provided model_version

        Args:
            model_version (str, run): model verison object
            dataset_versions (list(str, run)): list of dataset version objects  
        """
        if len(dataset_versions) > 0:
                dataset_arr = [self.get_resource_id(dv) for dv in dataset_versions]
                self.log_tag(model_version, "dataset_versions", dataset_arr)
                self.log_tag(model_version, "dataset_versions.exists", "True")
        else: #if we're training w/o generating data (for some reason?) then just try to get data from the last model version
            model_verison_id = self.get_resource_id(model_version)
            prev_model_version = self.get_prev_resource_version(model_version, extra_filters=[
                                                                "tags.%s.dataset_versions.exists = 'True'" % model_verison_id])
            if prev_model_version is not None: 
                dataset_verisons = self.get_metadata(prev_model_version, id="dataset_versions")
                if dataset_verisons is not None: 
                    self.log_tag(model_version, "dataset_versions",dataset_verisons)
                    #self.log_tag(model_version, "dataset_versions.exists", "True")
            else: 
                self.log("Unable to find previous model version with lineage for model : %s" %self.get_resource_id(model_version))


    #resource is tuple (resource, run)
    def get_resource_id(self, resource, *args, **kwargs):
        """Returns the id of a given resource

        Args:
            resource (str, run): Any resource created by this metadata tracker

        Returns:
            str: resource id
        """
        resource_out = resource[0]    

        if "/" in resource_out:
            #use file name 
            resource_out = str(Path(resource_out).stem).replace(".", "_")
        
        #run_id = resource[1].info.run_id
        #resource_out = "%s_%s" %(resource_out, run_id)

        return resource_out

    def get_parent_id(self, resource, type=None, *args, **kwargs):
        """Returns the parent id of a resource. Note that currently only 
        experiments have a proper parent, but this could be extended in the future. 

        Args:
            resource (str, run): Any resource object 
            type (str, optional): rsource type. Defaults to None.

        Returns:
            parent_id: str, or None
        """
        id = resource[0]
        if type == "experiment": 
            _, model_id = id.split(".")
            return model_id 
        else: #there's no real heirarchy other than this in the mlflow implementation
            return None 
        
    def register_vc_resource(self, resource, vc_info, key=None, additional_metadata={}, *args, **kwargs):
        """Registers information received from a resource version control component into the metadata tracker

        Args:
            resource (str, run): Resource to log vc_info into
            vc_info (dict): dictionary of information returned by the version control component
            key (str, optional): key to append to values to be logged. Defaults to None.
            additional_metadata (dict, optional): additionally metadat to log. Defaults to {}.
        """
        #check if a git commit is present. if so then we know we did an external save
        if vc_info and "hexsha" in vc_info.keys():
            uri = vc_info.get("uri")
            hexsha = vc_info.get("hexsha")

            id = self.get_resource_id(resource)
            if "." not in id: #don't log experiment existance
                self.log_tag(resource, "exists", "True")
            hexsha_key="hexsha"
            if key is not None: 
                hexsha_key = "%s_hexsha" %key
            uri_key="uri"
            if key is not None: 
                uri_key = "%s_uri" %key
            self.log_tag(resource, hexsha_key, hexsha)
            self.log_tag(resource, uri_key, uri)
            #log this so we can search on existance of resource in past runs 

        if len(additional_metadata) > 0:
            for k, v in additional_metadata.items():
                self.log_metadata(resource, id=k, data=v)

    def get_vc_info(self, resource, key="hexsha", *args, **kwargs):
        """Returns the resource version control information that was previously logged

        Args:
            resource (str, run): resource to fetch vc_info from
            key (str, optional): key used when saving vc_info. Defaults to "hexsha".

        Returns:
            vc_info: Returns the information needed to retrieve object from the version 
            control system. This will typically be something like a git hexsha
        """
        vc_info = {"hexsha": self.get_tag(resource, key)}
        return vc_info 

    def log_data_profile(self, resource, file_path, *args, **kwargs):
        """logs a data profile to resource

        Args:
            resource (str, run): The resource to log the data profile into
            file_path (str): file path of the data profile
        """
        id = self.get_resource_id(resource)
        id = id + "_data_profile"
        self.log_artifact(resource, id, file_path)
        
    def get_data_profile(self, resource, id, *args, **kwargs):
        pass

    def log_checks(self, resource, file_path, type="data", *args, **kwargs):
        """Logs a data check into a resource

        Args:
            resource (_type_): resource to log into
            file_path (_type_): file path of the check
            type (str, optional): type of check. Defaults to "data".
        """
        id = self.get_resource_id(resource)
        id = id + "_%s_checks_report" %type
        self.log_artifact(resource, id, file_path)

    def get_data_checks(self, resource, id, *args, **kwargs):
        pass

    def log_data_comparison(self, resource, file_path, *args, **kwargs):
        """Logs a data comparison into a resource

        Args:
            resource (str, run): resource to log into
            file_path (str): file path of the data comparision
        """
        id = self.get_resource_id(resource)
        id = id + "_data_comparison"
        self.log_artifact(resource, id, file_path)

    def stop(self, *args, **kwargs):
        """Stop the metadata tracker run. 
        """
        mlflow_utils.stop_run(self.run.info.run_id, self.run.info.experiment_id)

    #should this live in model_repository?
    def load_model(self, model_obj, model_version, ref_model, pipeline_config={}, *args, **kwargs):
        """Load a model trainer object from the metadata tracker

        Args:
            model_obj (object): A fitted model 
            model_version (str, run): The model version to use to retrieve the model trainer
            ref_model (object): A model trainer object to use as a reference. I.E. will have similar configs, etc.
            pipeline_config (dict, optional): pipeline config to pass. Defaults to {}.

        Returns:
            model: the model trainer object
        """
        model_trainer = self.get_metadata(model_version, "winning_experiment_model_trainer")
        model_cl = utils.load_class(model_trainer)
        dependent_components = {"logger": self.logger, "notifier": self.notifier,  "metadata_tracker": self.metadata_tracker,
                                "metrics_tracker": self.metrics_tracker, "resource_version_control": self.resource_version_control}
        #might want to find a better way to do this next step.
        #it would be nice if you could reconstruct a model trainer class only w/ a model version object
        if ref_model is not None:
            config = ref_model.config
            parent_process = ref_model.parent_process
            params = ref_model.params
            pipeline_conf = ref_model.pipeline_conf
        else:
            config = {}
            parent_process = self.parent_process
            params = {}
            pipeline_conf = {}
        if len(pipeline_config) > 0:
            pipeline_conf = pipeline_config 
        
        model = model_cl(conf=config, pipeline_conf=pipeline_conf, runner_conf=self.runner_conf, parent_process=parent_process,
                         problem_type=self.problem_type, params=params, components=dependent_components)
        #if you passed in a model_obj, we assume you have a pre-trained model object you wish to use
        if model_obj is not None:
            model._set_model(model_obj)
        return model
