from lolpop.component.model_repository.base_model_repository import BaseModelRepository
from lolpop.utils import common_utils as utils
from lolpop.component.metadata_tracker.continual_metadata_tracker import ContinualMetadataTracker
from lolpop.utils import continual_utils as cutils

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ContinualModelRepository(BaseModelRepository):
    __REQUIRED_CONF__ = {
        "components": ["metadata_tracker|ContinualMetadataTracker"],
        "config": []
    }

    def __init__(self, description=None, run_id=None, components={}, *args, **kwargs):
        #set normal config
        super().__init__(components=components, *args, **kwargs)

        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case.
        if isinstance(components.get("metadata_tracker"), ContinualMetadataTracker):
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else:
            secrets = utils.load_config(["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT",
                                        "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"], self.config)
            self.client = cutils.get_client(secrets)
            self.run = cutils.get_run(
                self.client, description=description, run_id=run_id)

    def register_model(self, model_version, model, *args, **kwargs):
        #only supports the Continual Metadata Tracker, so model is already in the system.
        return model_version

    def promote_model(self, model_version, reason="UPLIFT", *args, **kwargs):
        improvement_metric = self.metrics_tracker.get_metric_value(
            model_version, "performance_metric_name")
        improvement_metric_value = self.metrics_tracker.get_metric_value(model_version,"performance_metric_val")
        try: 
            improvement_metric_diff = self.metrics_tracker.get_metric_value(model_version, "deployed_model_perf_metric_diff")
        except: #this fails if the model is the first model, as there is no comparison to the previous model 
            improvement_metric_diff = 0 
        base_improvement_metric_value = improvement_metric_value - improvement_metric_diff
        promotion = self.metadata_tracker.create_resource(
            improvement_metric=improvement_metric, 
            improvement_metric_value=improvement_metric_value, 
            base_improvement_metric_value=base_improvement_metric_value, 
            #improvement_metric_diff=improvement_metric_diff,
            id=None, parent=model_version, type="promotion", reason=reason)
        return promotion

    #approvals are not implemented in Continual, so just return True if called.
    def check_approval(self, promotion, *args, **kwargs):
        return True

    def approve_model(self, promotion, *args, **kwargs):
        return True
