from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseModelExplainer(BaseComponent): 
    __REQUIRED_CONF__ = {
        "config" : []
    }
    
    def get_feature_importance(self, data, model, *args, **kwargs) -> tuple[Any, Any]: 
        pass 

    def get_explanations(self, data, model, *args, **kwargs) -> Any:
        pass 