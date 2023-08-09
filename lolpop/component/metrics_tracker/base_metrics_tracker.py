from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseMetricsTracker(BaseComponent): 

    url = "https://replace.me"

    def log_metric(self, resource, id, value, *args, **kwargs): 
        pass 

    def get_metric(self, resource, id, *args, **kwargs) -> Any:
        pass

    def log_metrics(self, resource, metrics, *args, **kwargs):
        pass

    def copy_metrics(self, from_resource, to_resource, *args, **kwargs):
        pass

    def log_prediction_metrics(self, prediction_resource, predictions, *args, **kwargs):
        pass
