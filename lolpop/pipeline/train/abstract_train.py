from lolpop.pipeline.abstract_pipeline import AbstractPipeline
from lolpop.utils import common_utils as utils

class AbstractTrain(AbstractPipeline): 
    def __init__(self, conf, runner_conf, pipeline_type = "train", **kwargs):
        super().__init__(conf, runner_conf, pipeline_type = pipeline_type, **kwargs)

    def split_data(self, data, *args, **kwargs): 
        pass 

    def train_model(self, data, *args, **kwargs): 
        pass 

    def analyze_model(self, *args, **kwargs): 
        pass 

    def check_model(self, *args, **kwargs):
        pass

    def compare_models(self, *args, **kwargs):
        pass

    def deploy_model(self, *args, **kwargs):
        pass
