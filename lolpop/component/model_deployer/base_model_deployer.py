from lolpop.component.base_component import BaseComponent

class BaseModelDeployer(BaseComponent): 

    def deploy_model(self, model, *args, **kwargs): 
        pass 

    def build_api(self, model, *args, **kwargs): 
        pass 

    def build_container(self, model, *args, **kwargs): 
        pass 

    def package_model(self, model, *args, **kwargs): 
        pass