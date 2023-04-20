from lolpop.component.abstract_component import AbstractComponent

class BaseMetricsTracker(AbstractComponent): 

    def log_metric(self, id, value, time, **kwargs): 
        pass 

    def get_metric(self, id, time, **kwargs):
        pass