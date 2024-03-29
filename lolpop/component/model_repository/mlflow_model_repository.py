from lolpop.component.model_repository.base_model_repository import BaseModelRepository
from lolpop.utils import common_utils as utils

from lolpop.component.metadata_tracker.mlflow_metadata_tracker import MLFlowMetadataTracker
from lolpop.utils import mlflow_utils
import mlflow


@utils.decorate_all_methods([utils.error_handler, 
                             utils.log_execution(), 
                             mlflow_utils.check_active_mlflow_run(mlflow)])
class MLFlowModelRepository(BaseModelRepository):
    __REQUIRED_CONF__ = {
        "component": ["metadata_tracker|MLFlowMetadataTracker"],
        "config": []
    }

    def __init__(self, dependent_integrations=None, *args, **kwargs):
        if dependent_integrations is None: 
            dependent_integrations = {}
        #set normal config
        super().__init__(dependent_integrations=dependent_integrations, *args, **kwargs)

        if isinstance(dependent_integrations.get("component",{}).get("metadata_tracker"), MLFlowMetadataTracker):
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
            self.url = self.metadata_tracker.url
        else:  # we should only use this if we allow metrics tracking w/o metadata tracking
            tracking_uri = self._get_config("mlflow_tracking_uri")
            experiment_name = self._get_config("mlflow_experiment_name")

            self.client, self.run = mlflow_utils.connect(
                tracking_uri, experiment_name)
            self.url = tracking_uri

            self.log("Using MLFlow in experiment %s with run id: %s" %(experiment_name, self.run.info.run_id), level="INFO")

    def register_model(self, model_version, model, *args, **kwargs):
        """ Registers model  in MLFlow and returns the name of the registered model.
        
        Args:
            model_version (object): the version of the model to register.
            model (object): the  model object to register.
            
        Returns:
            reg_name (str): the name of the registered model.
        """
        model_module = getattr(mlflow, model.mlflow_module.lower()) 

        model_id = self.metadata_tracker.get_resource_id(model_version)
        reg_name = model_id + "_reg"

        #note: if model is already registered, this will simply bump up the verison number
        model_module.log_model(model._get_model(), 
                               artifact_path = "%s_model" %model_id, 
                               registered_model_name=reg_name,
                               **kwargs)

        #log creation of the new model version. unfortunate log_model doesn't give back the right object
        registered_model_version = self.client.get_latest_versions(reg_name, stages=['None'])[0]
        self.log("Successfully logged model %s at version %s" %(reg_name, registered_model_version.version))

        self.metadata_tracker.log_metadata(model_version, id="status", data="REGISTERED")

        return reg_name

    def promote_model(self, registered_model_name, from_stage="None", to_stage="Production", demote_previous_model_versions=True, *args, **kwargs):
        """ Promotes the specified registered model to a given stage and logs the promotion in the metadata tracker.
        
        Args:
            registered_model_name (str): the name of the registered model to promote.
            from_stage (str): the starting stage of the registered model. Default is "None".
            to_stage (str): the target stage to promote the registered model to. Default is "Production".
            demote_previous_model_versions (bool): a boolean variable to enable or disable demotion of previous instances of the registered model. Default is True.
            *args: additional positional arguments.
            **kwargs: additional keyword arguments.
            
        Returns:
            model_version (tuple): a tuple containing the ID of the registered model and an MLFlow run object for the promoted model version.

        """
        registered_model_version = self.client.get_latest_versions(registered_model_name, stages=[from_stage])[0]

        self.client.transition_model_version_stage(
            name=registered_model_name,
            version=registered_model_version.version,
            stage = to_stage, 
            archive_existing_versions=demote_previous_model_versions,
        )

        self.log("Successfully transitioned model %s, version %s to stage %s" %(registered_model_name, registered_model_version.version, to_stage))

        model_version_id = get_model_id_from_reg_model(registered_model_version.name)
        model_status_tag = "%s.status" %model_version_id
        model_version = (model_version_id, self.client.get_run(run_id=registered_model_version.run_id))

        self.metadata_tracker.log_metadata(model_version, id="status", data="PROMOTED")

        if demote_previous_model_versions: 
            prev_version = self.metadata_tracker.get_prev_resource_version(model_version, extra_filters = ["tags.%s = 'DEPLOYED'" %model_status_tag], num=100)
            if prev_version is not None: 
                for run in prev_version[1]: 
                    self.metadata_tracker.log_metadata(model_version, id = "status", data="DEMOTED")

        return model_version

    #approvals are not implemented in mflow, so just return True if called.
    def check_approval(self, promotion, *args, **kwargs):
        return True

    def approve_model(self, promotion, *args, **kwargs):
        return True

def get_model_id_from_reg_model(reg_model): 
    return "_".join(reg_model.split("_")[:-1])