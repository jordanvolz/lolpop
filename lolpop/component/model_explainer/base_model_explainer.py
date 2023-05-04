from lolpop.component.base_component import BaseComponent

class BaseModelExplainer(BaseComponent): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    
    def get_feature_importance(self, data, model, *args, **kwargs): 
        pass 

