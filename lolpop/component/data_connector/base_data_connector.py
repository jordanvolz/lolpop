from lolpop.component.base_component import BaseComponent
from typing import Any

class BaseDataConnector(BaseComponent):

    def get_data(self, source, *args, **kwargs) -> Any:
        pass

    def save_data(self, data, target, *args, **kwargs):
        pass

    def _load_data(self, source, config, *args, **kwargs) -> Any: 
        pass

    def _save_data(self, data, config, *args, **kwargs): 
        pass 