from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseModelBiasChecker(BaseComponent): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    
    def check_model_bias(self, data, model, *args, **kwargs) -> Any: 
        pass 

