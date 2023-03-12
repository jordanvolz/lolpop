from lolpop.component.abstract_component import AbstractComponent

class AbstractModelDeployer(AbstractComponent): 

    def deploy_model(self, model, *args, **kwargs): 
        pass 

    def build_api(self, model, *args, **kwargs): 
        pass 

    def build_container(self, model, *args, **kwargs): 
        pass 

    def package_model(self, model, *args, **kwargs): 
        pass