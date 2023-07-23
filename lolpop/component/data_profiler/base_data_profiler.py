from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseDataProfiler(BaseComponent): 

    def profile_data(self, data, *args, **kwargs) -> tuple[Any, str]:
        pass 

    def compare_data(self, data, prev_data, *args, **kwargs)-> tuple[Any, str]:
        pass
