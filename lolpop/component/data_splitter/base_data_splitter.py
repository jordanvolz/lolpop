from lolpop.component.base_component import BaseComponent
from typing import Any

class BaseDataSplitter(BaseComponent): 

    def split_data(self, data, *args, **kwargs) -> dict[str, Any]: 
        pass 

    def get_train_test_dfs(self, data, *args, **kwargs) -> tuple[Any, Any]: 
        pass 
