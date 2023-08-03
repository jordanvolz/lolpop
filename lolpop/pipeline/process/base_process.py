from lolpop.pipeline.base_pipeline import BasePipeline
from typing import Any 

class BaseProcess(BasePipeline): 

    datasets_used = []

    def __init__(self, pipeline_type = "process", *args, **kwargs):
        super().__init__(pipeline_type=pipeline_type, *args, **kwargs)

    def transform_data(self, source, *args, **kwargs) -> Any: 
        pass 

    def track_data(self, data, id, *args, **kwargs) -> Any: 
        pass

    def profile_data(self, data, dataset_version, *args, **kwargs): 
        pass 

    def check_data(self, data, dataset_version, *args, **kwargs): 
        pass 

    def compare_data(self, data, dataset_version, *args, **kwargs): 
        pass 

