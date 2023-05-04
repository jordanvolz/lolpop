from lolpop.component.base_component import BaseComponent

class BaseMetricsTracker(BaseComponent): 

    def log_metric(self, id, value, time, **kwargs): 
        pass 

    def get_metric(self, id, time, **kwargs):
        pass