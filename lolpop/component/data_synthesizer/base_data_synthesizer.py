from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseDataSynthesizer(BaseComponent):

    def load_data(self, source_file, *args, **kwargs) -> tuple[Any, Any]:
        pass

    def model_data(self, data, *args, **kwargs) -> Any:
        pass

    def sample_data(self, model, num_rows, *args, **kwargs) -> Any:
        pass

    def evaluate_data(self, real_data, synthetic_data, *args, **kwargs) -> list[Any]:
        pass
