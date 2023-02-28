from pipeline.deploy.abstract_deploy import AbstractDeploy
from utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class OfflineDeploy(AbstractDeploy):

    def __init__(self, conf, runner_conf, **kwargs):
        super().__init__(conf, runner_conf, **kwargs)

    def promote_model(self, model_version, model=None, *args, **kwargs):
        #get model from RVC if not provided.
        if model is None:
            if model_version is not None:
                experiment = self.metadata_tracker.get_winning_experiment(
                    model_version)
                model = self.resource_version_control.get_model(experiment)

        #register model in model repository
        model_id = self.model_repository.register_model(model_version, model)

        #promote model
        promotion = self.model_repository.promote_model(model_id)

        return promotion

    def check_approval(self, promotion, *args, **kwargs):
        is_approved = self.model_repository.check_approval(promotion)

        if not is_approved and self._get_config("auto_approve_models"):
            self.approve_model(promotion)
            is_approved = True

        return is_approved

    def approve_model(self, promotion, *args, **kwargs):
        approval = self.model_repository.approve_model(promotion)
        return approval

    def deploy_model(self, promotion, model_version, *args, **kwaargs):
        deployment = self.model_deployer.deploy_model(promotion, model_version)
        return deployment
