from lolpop.pipeline.deploy.base_deploy import BaseDeploy
from lolpop.utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class OfflineDeploy(BaseDeploy):

    __REQUIRED_CONF__ = {
        "components" : [
            "metadata_tracker", 
            "resource_version_control", 
            "model_repository", 
            "model_deployer"
            ]
    }

    def promote_model(self, model_version, model=None, *args, **kwargs):
        """
        Promotes a model to model repository.

        Args:
            model_version (int): The version of the model to be promoted.
            model (object): The model object to be promoted (Optional).
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            promotion (object): The promotion object that contains information about the promoted model.

        Raises:
            None.
        """
        #get model from RVC if not provided.
        if model is None:
            if model_version is not None:
                experiment = self.metadata_tracker.get_winning_experiment(model_version)
                model_obj = self.resource_version_control.get_model(experiment)
                model = self.metadata_tracker.load_model(model_obj, model_version, ref_model=None)
            else: 
                self.notify("Must provide either model_version or model in order to promote a model.")

        #register model in model repository
        model_id = self.model_repository.register_model(model_version, model)

        #promote model
        promotion = self.model_repository.promote_model(model_id)

        return promotion

    def check_approval(self, promotion, *args, **kwargs):
        """
        Checks if the given model promotion is approved in the model repository.

        Args:
            promotion (object): The promotion object that contains information about the promoted model.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            is_approved (bool): True if the promotion is approved, False otherwise.

        Raises:
            None.
        """
        is_approved = self.model_repository.check_approval(promotion)

        if not is_approved and self._get_config("auto_approve_models"):
            self.approve_model(promotion)
            is_approved = True

        return is_approved

    def approve_model(self, promotion, *args, **kwargs):
        """
        Approves the given model promotion in the model repository.

        Args:
            promotion (object): The promotion object that contains information about the promoted model.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            approval (object): The approval object that contains information about the approved model promotion.

        Raises:
            None.
        """
        approval = self.model_repository.approve_model(promotion)
        return approval

    def deploy_model(self, promotion, model_version, *args, **kwargs):
        """
        Deploys the given model promotion.

        Args:
            promotion (object): The promotion object that contains information about the promoted model.
            model_version (int): The version of the model to be deployed.
            *args: Variable length argument list.
            **kwaargs: Arbitrary keyword arguments.

        Returns:
            deployment (object): An object that contains information about the deployed model.

        Raises:
            None.
        """
        deployment = self.model_deployer.deploy_model(promotion, model_version)
        return deployment
