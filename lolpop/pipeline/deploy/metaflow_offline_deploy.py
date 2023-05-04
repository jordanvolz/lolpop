from lolpop.pipeline.deploy.base_deploy import BaseDeploy
from lolpop.utils import common_utils as utils
from lolpop.utils import metaflow_utils as meta_utils
from metaflow import FlowSpec, step
from pathlib import Path

METAFLOW_CLASS = "MetaflowOfflineDeploySpec"
PLUGIN_PATHS = "plugin_paths.txt"

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowOfflineDeploy(BaseDeploy):

    def run(self, model, model_version, **kwargs):
        #get flow class object from this file
        mod_cl = meta_utils.get_flow_class(__file__, METAFLOW_CLASS)

        flow = meta_utils.load_flow(
            mod_cl, self, PLUGIN_PATHS, model=model, model_version=model_version)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)

        meta_utils.run_flow(flow, "run", __file__, PLUGIN_PATHS)
        self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)

    def get_artifacts(self, artifact_keys):
        #get latest run of this pipeline
        run = meta_utils.get_latest_run(METAFLOW_CLASS)

        #get requested artifacts
        artifacts = meta_utils.get_run_artifacts(
            run, artifact_keys, METAFLOW_CLASS)

        return artifacts


class MetaflowOfflineDeploySpec(FlowSpec):

    def __init__(self, lolpop=None, model=None, model_version=None, use_cli=False, **kwargs):
        #you need to set local attributes before calling super
        #only the first time we create the class will these parameters be provided.
        #The rest of the calls are metaflow internal calls and we do not want to reset them
        if lolpop is not None:
            self.lolpop = lolpop
        if model is not None:
            self.model = model
        if model_version is not None: 
            self.model_version = model_version

        #load plugins
        meta_utils.load_plugins(PLUGIN_PATHS)

        #call init -- this kicks off the main workflow
        super().__init__(use_cli=use_cli)

    @step
    def start(self):
        self.next(self.promote_model)

    @step
    def promote_model(self):
        #get model from RVC if not provided.
        if self.model is None:
            if self.model_version is not None:
                experiment = self.lolpop.metadata_tracker.get_winning_experiment(
                    self.model_version)
                model_obj = self.lolpop.resource_version_control.get_model(experiment)
                self.model = self.lolpop.metadata_tracker.load_model(
                    model_obj, self.model_version, ref_model=None)
            else:
                self.lolpop.notify(
                    "Must provide either model_version or model in order to promote a model.")

        #register model in model repository
        model_id = self.lolpop.model_repository.register_model(self.model_version, self.model)

        #promote model
        promotion = self.lolpop.model_repository.promote_model(model_id)
        self.promotion = promotion 

        self.next(self.check_approval)

    @step
    def check_approval(self):
        is_approved = self.lolpop.model_repository.check_approval(self.promotion)

        if not is_approved and self.lolpop._get_config("auto_approve_models"):
            self.lolpop.model_repository.approve_model(self.promotion)
            is_approved = True

        self.is_approved = is_approved

        self.next(self.deploy_model)

    @step
    def deploy_model(self):
        if self.is_approved: 
            deployment = self.lolpop.model_deployer.deploy_model(self.promotion, self.model_version)
            self.deployment = deployment

        self.next(self.end)

    @step
    def end(self):
        pass
    

if __name__ == '__main__':
    #need to use CLI here because metaflow calls back into this function to
    #execute each individual step
    MetaflowOfflineDeploySpec(use_cli=True)
