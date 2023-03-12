from lolpop.component.abstract_component import AbstractComponent

class AbstractModelBiasChecker(AbstractComponent): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    
    def check_model_bias(self, data, model, *args, **kwargs): 
        pass 

