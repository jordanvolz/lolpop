from component.abstract_component import AbstractComponent

class AbstractMetricsTracker(AbstractComponent): 

    def log_metric(self, id, value, time, **kwargs): 
        pass 

    def get_metric(self, id, time, **kwargs):
        pass