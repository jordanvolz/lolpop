from lolpop.pipeline.base_pipeline import BasePipeline
from typing import Any 

class BasePredict(BasePipeline): 
    def __init__(self, pipeline_type="predict", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)

    def compare_data(self, model_version, dataset_version, data, *args, **kwargs):
        pass

    def get_predictions(self, model, model_version, data, *args, **kwargs) -> tuple[Any, Any]:
        pass 

    def track_predictions(self, prediction_job, data, *args, **kwargs):
        pass 

    def analyze_prediciton_drift(self, dataset_version, prediction_job, data, *args, **kwargs):
        pass 

    def check_predictions(self, data, prediction_job,  *args, **kwargs):
        pass 

    def save_predictions(self, data, target, *args, **kwargs):
        pass 