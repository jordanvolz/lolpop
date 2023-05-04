from lolpop.component.base_component import BaseComponent

class BaseModelBiasChecker(BaseComponent): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    
    def check_model_bias(self, data, model, *args, **kwargs): 
        pass 

