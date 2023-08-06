from lolpop.pipeline.base_pipeline import BasePipeline
from lolpop.utils import common_utils as utils
from typing import Any 

class BaseTrain(BasePipeline): 
    def __init__(self, pipeline_type = "train", *args, **kwargs):
        super().__init__(pipeline_type = pipeline_type, *args, **kwargs)

    def split_data(self, data, *args, **kwargs) -> Any: 
        pass 

    def train_model(self, data, *args, **kwargs) -> tuple[Any, Any]: 
        pass 

    def check_model(self, data, model, model_version, *args, **kwargs):
        pass

    def analyze_model(self, data, model, model_verison, *args, **kwargs):
        pass

    def compare_models(self, data, model, model_version, *args, **kwargs) -> bool:
        pass

    def check_model_bias(self, data, model, model_version, *args, **kwargs):
        pass

    def retrain_model_on_all_data(self, data, model_version, *args, **kwargs) -> tuple[Any, Any]: 
        pass 
