from component.model_repository.abstract_model_repository import AbstractModelRepository
from utils import common_utils as utils
from component.metadata_tracker.continual_metadata_tracker import ContinualMetadataTracker
from utils import common_utils as utils
from utils import continual_utils as cutils

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ContinualModelRepository(AbstractModelRepository):
    __REQUIRED_CONF__ = {
        "components": ["metadata_tracker|ContinualMetadataTracker"],
        "config": []
    }

    def __init__(self, conf, pipeline_conf, runner_conf, description=None, run_id=None, **kwargs):
        #set normal config
        super().__init__(conf, pipeline_conf, runner_conf, **kwargs)

        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case.
        if isinstance(kwargs.get("components", {"metadata_tracker": None}).get("metadata_tracker"), ContinualMetadataTracker):
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else:
            secrets = utils.load_config(["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT",
                                        "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"], conf.get("config", {}))
            self.client = cutils.get_client(secrets)
            self.run = cutils.get_run(
                self.client, description=description, run_id=run_id)

    def register_model(self, model_version, model, *args, **kwargs):
        #only supports the Continual Metadata Tracker, so model is already in the system.
        return model_version

    def promote_model(self, model_version, reason="UPLIFT", *args, **kwargs):
        promotion = self.metadata_tracker.create_resource(
            model_version, type="promotion", reason=reason)
        return promotion

    #approvals are not implemented in Continual, so just return True if called.
    def check_approval(self, promotion, *args, **kwargs):
        return True

    def approve_model(self, promotion, *args, **kwargs):
        return True
