from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseDataTransformer(BaseComponent): 

    def transform(self, source, *args, **kwargs) -> Any:
        pass
