from lolpop.component.base_component import BaseComponent

class BaseMetricsTracker(BaseComponent): 

    def log_metric(self, id, value, time, *args, **kwargs): 
        pass 

    def get_metric(self, id, time, *args, **kwargs):
        pass

    def log_metrics(self, id, time, *args, **kwargs):
        pass

    def copy_metrics(self, id, time, *args, **kwargs):
        pass

    def log_prediction_metrics(self, id, time, *args, **kwargs):
        pass
