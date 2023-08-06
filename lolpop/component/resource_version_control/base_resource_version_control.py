from lolpop.component.base_component import BaseComponent
from typing import Any 

class BaseResourceVersionControl(BaseComponent): 

    def version_data(self, dataset_version, data, *args, **kwargs) -> dict[str, Any]: 
        pass 

    def get_data(self, dataset_version,  *args, **kwargs) -> Any :
        pass

    def version_model(self, experiment, model, *args, **kwargs) -> dict[str, Any]:
        pass
    
    def get_model(self, experiment, *args, **kwargs) -> Any : 
        pass
