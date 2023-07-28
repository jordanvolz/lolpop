from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseModelRepository(BaseComponent): 

    def register_model(self, model_version, model, *args, **kwargs) -> Any: 
        pass 

    def promote_model(self, id, *args, **kwargs): 
        pass 

    def approve_model(self, id, *args, **kwargs): 
        pass 

    def check_approva(self, id, *args, **kwargs) -> bool: 
        pass