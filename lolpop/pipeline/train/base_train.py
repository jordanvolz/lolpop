from lolpop.pipeline.base_pipeline import BasePipeline
from lolpop.utils import common_utils as utils

class BaseTrain(BasePipeline): 
    def __init__(self, pipeline_type = "train", *args, **kwargs):
        super().__init__(pipeline_type = pipeline_type, *args, **kwargs)

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
