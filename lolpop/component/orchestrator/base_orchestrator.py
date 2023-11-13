from lolpop.component.base_component import BaseComponent
from typing import Any

class BaseOrchestrator(BaseComponent):

    def decorator(self, func, cls) -> Any:
       pass

    def package(self, lolpop_class, lolpop_module, lolpop_entrypoint, *args, **kwargs) -> None:
        pass 

    def deploy(self, deployment_name, *args, **kwargs) -> None:
        pass
    
    def run(self, deployment_name, *args, **kwargs) -> tuple[str, str]:
        pass 
       
    def stop(self, deployment_name, *args, **kwargs) -> None:
        pass