from lolpop.component.base_component import BaseComponent
from typing import Any

class BaseDataChecker(BaseComponent): 

    def check_data(self, data, *args, **kwargs) -> tuple[Any, str, str]: 
        pass 

