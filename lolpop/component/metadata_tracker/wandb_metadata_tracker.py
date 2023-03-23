from lolpop.component.metadata_tracker.base_metadata_tracker import BaseMetadataTracker
from lolpop.utils import common_utils as utils
import wandb
import pandas as pd

#@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class WandBMetadataTracker(BaseMetadataTracker):
    __REQUIRED_CONF__ = {
        "config": ["WANDB_KEY", "WANDB_PROJECT", "WANDB_ENTITY"]
    }

    def __init__(self, conf, pipeline_conf, runner_conf, description=None, run_id=None, *args, **kwargs):
        #set normal config
        super().__init__(conf, pipeline_conf, runner_conf, *args, **kwargs)

        secrets = utils.load_config(
            ["WANDB_KEY", "WANDB_PROJECT", "WANDB_ENTITY"], conf.get("config", {}))

        self.client = wandb

        wandb.login(key=secrets.get("WANDB_KEY","WANDB_PROJECT"))

        self.run = wandb.init(project=secrets.get("WANDB_PROJECT"), id=run_id)

        self.api = wandb.Api() 

        self.log("Using Weights and Biases with run id: %s and name: %s" % (self.run.id, self.run.name), level="INFO")

        self.url = self.run.url

    def __exit__(self):
        self.stop()

    def log_artifact(self, id,  path=None, uri=None, external=False, key=None, type=None, *args, **kwargs):
        id = "%s_%s" %(id,key)
        artifact = wandb.Artifact(id, type=type)
        self.log("Weights & Baises artifact created: %s" % artifact.name)
        if not external: 
            artifact.add_file(path)
        else: 
            artifact.add_reference(uri)
        artifact.metadata.update(kwargs)
        
        self.run.log_artifact(artifact)
        #calling wait populates many artifact fields, which we may later want to use
        artifact.wait()
        self.log("Weights & Baises artifact logged: %s" % artifact.name)

        return artifact

    def get_artifact(self, resource, id, version="latest", *args, **kwargs):
        """Retrieves an artifact from W&B. 

        Args:
            resource (_type_): Not used
            id (Strign): Artifact name
            version (str, optional): Artifact version. Defaults to "latest".

        Returns:
            _type_: _description_
        """
        id = "%s:%s" %(id, version)
        artifact = self.run.use_artifact(id)
        return artifact

    def log_metadata(self, resource, id, data, *args, **kwargs):
        """Logs metadata to the W&B run. 

        Args:
            resource (String): resource type
            id (String): metadata id 
            data (dict): metadata 

        Returns:
            _type_: _description_
        """
        key = "%s|%s" % (resource, id)
        self.run.log(key, data)
        self.log("Weights and Biases metadata created: %s" % key)
        return key

    def get_metadata(self, resource, id, *args, **kwargs):
        key = "%s|%s" % (resource, id)
        data = self.run.summary.get(key)
        return data

    def log_tag(self, resource, tag, *args, **kwargs):
        key = "%s|%s" % (resource, tag)
        self.run.tags = self.run.tags + (key,)
        self.log("Added Weights and Biases tag: %s" % key)
        
    def get_tag(self, resource, key, **kwargs):
        key = "%s|%s" % (resource, tag)
        return key

    #this is basically a no-op. W&B doesn't let you log an artifact multiple times in a run, so
    # we basically just no-op this and do all the work in log_artifact. 
    def create_resource(self, id, type=None, parent=None, **kwargs):
        if type == "dataset_version": 
            type="dataset"
        elif type == "model_version": 
            type="model"
        elif type == "experiment": 
            id = parent(0)

        #self.log("Weights & Baises artifact created: %s" % artifact.name)
        #return artifact 
        return (id, type) 

    def get_resource(self, id, type, parent=None):
        return type

    def update_resource(self, resource, value_dict, type=None):
        return resource

    def get_prev_resource_version(self, artifact):
        previous_artifact = None 

        artifact_name, current_version = artifact.name.split(":") 
        current_version_num = int(current_version[1:])
        if current_version_num > 0: 
            previous_version = "v" + str(current_version_num-1)

        previous_artifact = wandb.use_artifact("%s:%s" %(artifact_name, previous_version))

        return previous_artifact

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
            resource = model.batch_predictions.list(
                default_sort_order="DESC")[0]
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
            dataset_dict = {x: y for x, y in zip(
                range(len(dataset_arr)), dataset_arr)}
            self.log_metadata(
                model_version, id="dataset_versions", data=dataset_dict)
        else:
            prev_model_version = self.get_prev_resource_version(model_version)
            dataset_verisons = self.get_metadata(
                prev_model_version, id="dataset_versions") or {}
            for v in dataset_verisons.keys():
                dataset_version = self.get_resource(v, type="dataset_version")
                dv.assignments.create(resource_name=model_version.name)

    def get_resource_id(self, resource, *args, **kwargs):
        return resource(0)

    def get_parent_id(self, resource, *args, **kwargs):
        return resource.parent.split("/")[-1]

    def register_vc_resource(self, resource, vc_info, key=None, additional_metadata={}, **kwargs):
        #check if a git commit is present. if so then we know we did an external save
        if "hexsha" in vc_info.keys():
            uri = vc_info.get("uri")
            hexsha = vc_info.get("hexsha")

            id = resource(0)
            type = resource(1)
            artifact = self.log_artifact(
                id, url=uri,  type=type, external=True, hexsha=hexsha, **kwargs.update(additional_metadata))

    def get_vc_info(self, artifact, key="git_hexsha"):
        data = None
        metadata = artifact.metadata
        if metadata is not None:
            data = metadata.get("hexsha")
        return {"hexsha" : data}

    def log_data_profile(self, artifact, file_path, profile, profiler_class=None):
        table = wandb.Table(columns=["Data Profile"])
        table.add_data(wandb.Html(file_path))
        self.run.log({"%s_%s" %(artifact.name, "profile"): table})

        self.log("Logged %s data profile to Weights & Baises table" %(profiler_class))
        
        return table 

    def log_checks(self, artifact, file_path, report, checker_class=None, type="data"):
        table = wandb.Table(columns=["%s Checks" %type.title()])
        table.add_data(wandb.Html(file_path))
        self.run.log({"%s_%s_%s" %(artifact.name, type, "checks"): table})

        self.log("Logged %s data profile to Weights & Baises table" %
                 (checker_class))

        return table

    def log_data_comparison(self, artifact, file_path, report, profiler_class=None):
        table = wandb.Table(columns=["Data Comparison"])
        table.add_data(wandb.Html(file_path))
        self.run.log({"%s_%s" % (artifact.name, "comparison"): table})

        self.log("Logged %s data comparison to Weights & Baises table" %
                 (profiler_class))

    def get_winning_experiment(self, model_version):
        winning_exp_id = self.metadata_tracker.get_metadata(
            model_version, "winning_experiment_id").get("winning_experiment_id")
        experiment = self.metadata_tracker.get_resource(
            winning_exp_id, type="experiment", parent=model_version)
        return experiment

    def stop(self):
        wandb.finish()
