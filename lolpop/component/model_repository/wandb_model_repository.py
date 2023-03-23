from lolpop.component.model_repository.abstract_model_repository import AbstractModelRepository
from lolpop.utils import common_utils as utils
from lolpop.component.metadata_tracker.wandb_metadata_tracker import WandBMetadataTracker
from lolpop.utils import continual_utils as cutils

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class WandBModelRepository(AbstractModelRepository):
    __REQUIRED_CONF__ = {
        "components": ["metadata_tracker|WandBMetadataTracker"],
        "config": []
    }

    def __init__(self, conf, pipeline_conf, runner_conf, description=None, run_id=None, components={}, **kwargs):
        #set normal config
        super().__init__(conf, pipeline_conf, runner_conf, components=components, **kwargs)

        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case.
        if isinstance(components.get("metadata_tracker"), WandBMetadataTracker):
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else:
            secrets = utils.load_config(
                "WANDB_KEY", "WANDB_PROJECT", "WANDB_ENTITY", conf.get("config", {}))
            self.client = wandb
            wandb.login(key=secrets.get("WANDB_KEY", "WANDB_PROJECT"))
            self.run = wandb.init(
                project=secrets.get("WANDB_PROJECT"), id=run_id)

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
