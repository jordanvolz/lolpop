from lolpop.component.base_component import BaseComponent
from typing import Any


class BaseFeatureTransformer(BaseComponent):

    def fit(self, data, *args, **kwargs) -> Any: 
        pass 

    def transform(self, data, *args, **kwargs) -> Any:
        pass

    def save(self, target, *args, **kwargs):
        pass

    def load(self, source, *args, **kwargs) -> Any:
        pass

