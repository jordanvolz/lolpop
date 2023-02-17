from component.abstract_component import AbstractComponent

class AbstractModelExplainer(AbstractComponent): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    
    def get_feature_importance(self, data, model, *args, **kwargs): 
        pass 

