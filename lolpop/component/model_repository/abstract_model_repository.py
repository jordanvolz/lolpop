from lolpop.component.abstract_component import AbstractComponent

class AbstractModelRepository(AbstractComponent): 

    def register_model(self, model, *args, **kwargs): 
        pass 

    def promote_model(self, model, *args, **kwargs): 
        pass 

    def approve_model(self, model, *args, **kwargs): 
        pass 