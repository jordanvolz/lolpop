from lolpop.component.metadata_tracker.base_metadata_tracker import BaseMetadataTracker
from lolpop.utils import common_utils as utils
from lolpop.utils import continual_utils as cutils
import pandas as pd
import os 

#@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class ContinualMetadataTracker(BaseMetadataTracker): 
    """
    A class for logging metadata and artifacts to Continual. Inherits from BaseMetadataTracker.

    Args:
        conf (dict): Configuration dicitonary for the metadata tracker componenet.
        pipeline_conf (dict): Configuration dictionary for the pipeline.
        runner_conf (dict): Configuration dictionary for the runner.
        description (str, optional): Description for the run. Defaults to None.
        run_id (str, optional): ID of the run. Defaults to None.

    Attributes:
        __REQUIRED_CONF__: List of required configuration for this component. 
        client (): Client object for interacting with Continual.
        run (): Run object representing the current run in Continual.
        url (str): URL for the Continual application.
    """
    __REQUIRED_CONF__ = {
        "config" : ["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"]
    }

    def __init__(self, description=None, run_id=None, *args, **kwargs):
        """
        Initialize the ContinualMetadataTracker object.

        Args:
            conf (dict): Configuration dictionary for this component.
            pipeline_conf (dict): Configuration dictionary for the pipeline.
            runner_conf (dict): Configuration dictionary for the runner.
            description (str, optional): Description for the run. Defaults to None.
            run_id (str, optional): ID of the run. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        #set normal config
        super().__init__(*args, **kwargs)

        secrets = utils.load_config(["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"], self.config)
        
        self.client = cutils.get_client(secrets)
        
        self.run = cutils.get_run(self.client, description=description, run_id=run_id)

        self.log("Using Continual with run id: %s" %self.run.id, level="INFO")

        self.url = self.run.continual_app_url
    
    def __exit__(self):
        """
        Stop the ContinualMetadataTracker object.
        """
        self.stop()

    def log_artifact(self, resource,  **kwargs): 
        """
        Log an artifact to Continual.

        Args:
            resource: Resource object to log the artifact to. Typically should be an experiment, modelversion, or datasetversion object. 
            **kwargs: Arbitrary keyword arguments.

        Returns:
            artifact: The created Continual artifact object.
        """
        artifact = resource.artifacts.create(replace_if_exists=True, **kwargs)
        self.log("Continual artifact created: %s" %artifact.name)
        return artifact 

    def get_artifact(self, resource, id):
        """
        Retrieve a Continual artifact.

        Args:
            resource: Resource object the artifact belongs to.
            id (str): ID of the artifact to retrieve.

        Returns:
            artifact: The retrieved Continual artifact object.
        """
        artifact = resource.artifacts.get(id=id)
        return artifact 

    def log_metadata(self, resource, **kwargs):
        """
        Log metadata to Continual.

        Args:
            resource: Resource object to log the metadata to.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            metadata: The created Continual metadata object.
        """
        metadata = resource.metadata.create(replace_if_exists=True, **kwargs)
        self.log("Continual metadata created: %s" %metadata.name)
        return metadata 

    def get_metadata(self, resource,id):
        """
        Retrieve metadata from Continual.

        Args:
            resource: Resource object the metadata belongs to.
            id (str): ID of the metadata to retrieve.

        Returns:
            dict: The retrieved metadata dictionary.
        """
        data = None 
        try: 
            metadata = resource.metadata.get(id=id)
        except: 
            metadata = None 
        if metadata is not None: 
            data = metadata.data
        return data

    def log_tag(self, resource, key, value): 
        """
        Log a tag to Continual.

        Args:
            resource: Resource object to log the tag to.
            key (str): The key of the tag.
            value (str): The value of the tag.
        Returns:
            tag: The created tag object
        """
        tag = resource.tags.create(key=key, value=value)
        self.log("Continual tag created: %s" %tag.name)
        return tag
    
    def get_tag(self, resource, key, **kwargs):
        value = None
        tag = resource.tags.get(key=key)
        if tag is not None: 
            value = tag.value
        return value

    def create_resource(self, id, type=None, parent=None, **kwargs): 
        resource = None 
        if type == "dataset_version": 
            try: 
                resource = self.run.datasets.get(id).dataset_versions.create()
            except: 
                resource = self.run.datasets.create(id).dataset_versions.create()
        elif type == "dataset": 
            resource = self.run.datasets.create(id)
        elif type == "model_version":
            try: 
                resource = self.run.models.get(id).model_versions.create() 
            except: 
                resource = self.run.models.create(id).model_versions.create()  
        elif type == "experiment": 
            resource = parent.experiments.create()
        elif type == "promotion":
            resource = parent.promotions.create(
                reason = kwargs.get("reason", "UPLIFT"),
                model_version = parent.name,
                improvement_metric = kwargs.get("improvement_metric"),
                improvement_metric_value = kwargs.get("improvement_metric_value"),
                base_improvement_metric_value = kwargs.get(
                    "base_improvement_metric_value"),
                #improvement_metric_diff = kwargs.get("improvement_metric_diff")
                )
        elif type == "prediction_job": 
            resource = parent.batch_predictions.create(model_version=parent.name, prediction_count = kwargs.get("prediction_count")) 

        self.log("Get/Created Continual resource with name: %s" %resource.name, level="INFO")
        return resource

    def get_resource(self, id, type, parent=None): 
        resource = None 
        if type == "dataset_version": 
            resource = self.run.dataset_versions.get(id)
        elif type == "dataset": 
            resource = self.run.datasets.get(id)
        elif type == "experiment": 
            resource = self.run.model_versions.get(parent.name).experiments.get(id)
        elif type == "model": 
            resource = self.run.models.get(id)
        return resource

    def update_resource(self, resource, value_dict, type=None): 
        for k,v in value_dict.items():
            setattr(resource,k,v)
        resource.update(paths=value_dict.keys())

    def clean_resource(self, resource, type): 
        pass 

    def get_prev_resource_version(self, resource_version): 
        previous_resource_version = None
        name_arr = resource_version.name.split("/")
        # any resource version will have a slug ending in .../parent/parent_id/resource/id
        parent_resource_type = name_arr[-4] 
        parent_id = name_arr[-3]
        parent_resource = getattr(self.run,parent_resource_type).get(parent_id)
        resource_version_type = parent_resource_type[:-1] + "_" + name_arr[-2]
        recent_resource_version_list = getattr(parent_resource,resource_version_type).list(default_sort_order="DESC")

        found_current_version = False 
        i = 0
        while not found_current_version and i < len(recent_resource_version_list): 
            i+=1
            found_current_version = (recent_resource_version_list[i-1].name == resource_version.name)

        if found_current_version: 
            if i == len(recent_resource_version_list): #handle edge case where it was the last version in the list 
                previous_resource_version = getattr(parent_resource,resource_version_type).list(latest=True, page_size = len(recent_resource_version_list)+1)[-1]
            else: 
                previous_resource_version = recent_resource_version_list[i]    

        return previous_resource_version

    def get_currently_deployed_model_version(self, model_version, return_latest_if_no_deployed=True, **kwargs): 
        model = self.run.models.get(model_version.parent)
        deployed_mv = None
        try: 
            #get promoted model version
            latest_promotion = model.latest_promotion()
            if latest_promotion: 
                deployed_mv_name = latest_promotion.model_version
                #if no promotion, system returns this shell object, so check for that
                if len(deployed_mv_name) > 0: 
                    deployed_mv = model.model_versions.get(deployed_mv_name) 
            #if not promotion exists, return prior mv
            if deployed_mv is None and return_latest_if_no_deployed:
                deployed_mv = self.get_prev_resource_version(model_version)
        except: 
            deployed_mv = None         
        return deployed_mv

    def get_prediction_job_model_version(self, prediction_job): 
        model_version_name = prediction_job.model_version 
        model_version = self.run.model_versions.get(model_version_name)
        return model_version
    
    def get_latest_model_resource(self, model, type): 
        resource = None 
        if type == "prediction_job": 
            resource = model.batch_predictions.list(default_sort_order="DESC")[0]
        return resource

    #dataset versions should be populated by process pipeline and passed in by runner
    #if that doesn't happen, we can look up the last model version and reuse those dataset versions
    #this is technically not foolproof, but it's unclear how best to try to establish these relationships
    #otherwise. We need something like default level model relationships, or getting them via a feature store, etc 
    def build_model_lineage(self, model_version, dataset_versions): 
        if len(dataset_versions) > 0: 
            for dv in dataset_versions: 
                dv.assignments.create(resource_name=model_version.name)
                #when supported, we should add assignments to other things we want to track: 
                #<code>.py, requirements.txt, docker containers, etc
                #for now we an just log this as metadata/artifacts
            
            # turn datasets into a dict and save
            # we're doing this so from mv we can reference all datasets used from the model. 
            # This is useful when we want to be able to retrieve training data used later on
            dataset_arr = [dv.name for dv in dataset_versions]
            dataset_dict = {x:y for x,y in zip(range(len(dataset_arr)),dataset_arr)}
            self.log_metadata(model_version, id="dataset_versions", data=dataset_dict)
        else: 
            prev_model_version = self.get_prev_resource_version(model_version)
            dataset_verisons = self.get_metadata(prev_model_version, id="dataset_versions") or {}
            for v in dataset_verisons.keys(): 
                dataset_version = self.get_resource(v, type="dataset_version")
                dv.assignments.create(resource_name=model_version.name)


    def get_resource_id(self, resource, *args, **kwargs): 
        return resource.id

    def get_parent_id(self, resource, *args, **kwargs):  
        return resource.parent.split("/")[-1]

    def register_vc_resource(self, resource, vc_info, key=None, file_type="csv", additional_metadata = {}, **kwargs): 
        #check if a git commit is present. if so then we know we did an external save
        if "hexsha" in vc_info.keys(): 
            uri = vc_info.get("uri")
            hexsha = vc_info.get("hexsha")

            artifact = self.log_artifact(resource, id = key, url=uri, mime_type=file_type, external=True)
            self.log_metadata(resource, id="git_hexsha_%s" %key, data={"hexsha": hexsha})
        
        if len(additional_metadata) > 0: 
            for k,v in additional_metadata.items(): 
                self.log_metadata(resource, id = k, data=v)

    def get_vc_info(self, resource, key = "git_hexsha"): 
        data = None
        metadata = self.get_metadata(resource, key)
        if metadata is not None: 
            data = metadata.get("hexsha")
        return data

    def log_data_profile(self, resource, file_path, profile, profiler_class = None): 
        # in the future we may want to try to map the profile to Continual's internal profile type. 
        # we would do that via the profiler class and definining a mapping between objects 
        # but for now let's just register as an artifact and then we can view it in the UI

        if file_path is not None: # then we created a profile externally from Continual 
            artifact = self.log_artifact(resource, id="data-profile", path = file_path, external=False)
            return artifact
        elif profiler_class == "ContinualDataProfiler": 
            profile.get("dataframes")[0].info()
            data_profile = resource.data_profiles.create(**profile) #in this case, profile is a dict of arguments for the log_data_profile 
            self.log("Created Continual data profile: %s" %data_profile.name)
            return data_profile 

    def log_checks(self, resource, file_path, report, checker_class = None, type="data"): 
        # in the future we probably want to parse the report based on the checker_class
        # and then recreate checks in Continual. but for now we'll just register as an artifact

        if file_path is not None: # then we created a profile externally from Continual 
            artifact = self.log_artifact(resource, id="%s-checks-report" %type, path = file_path, external=False)
            return artifact

    def get_data_profile(self, resource, id):
        return self.get_artifact(resource, id) 

    def log_data_comparison(self, resource, file_path, report, profiler_class = None): 
        # in the future we may want to try to map the profile to Continual's internal metrics types. 
        # we would do that via the profiler class and definining a mapping between objects 
        # but for now let's just register as an artifact and then we can view it in the UI

        if file_path is not None: # then we created a profile externally from Continual 
            artifact = self.log_artifact(resource, id="data-comparison", path = file_path, external=False)
            return artifact
        elif profiler_class == "ContinualDataProfiler": 
            #not implemented
            return None

    def get_winning_experiment(self, model_version):
        winning_exp_id = self.metadata_tracker.get_metadata(model_version, "winning_experiment_id").get("winning_experiment_id")
        experiment = self.metadata_tracker.get_resource(winning_exp_id, type="experiment", parent=model_version)
        return experiment

    def stop(self):
        self.run.complete()
