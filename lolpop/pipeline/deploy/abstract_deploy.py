from lolpop.pipeline.abstract_pipeline import AbstractPipeline

class AbstractDeploy(AbstractPipeline): 
    def __init__(self, conf, runner_conf, pipeline_type="deploy", **kwargs):
        super().__init__(conf, runner_conf, pipeline_type=pipeline_type, **kwargs)

    def promote_model(self, model_version, *args, **kwargs): 
        pass 

    def deploy_model(self, model_version, *args, **kwaargs): 
        pass 

    def approve_model(self, model_version, *args, **kwargs): 
        pass 