from lolpop.base_integration import BaseIntegration

class BaseComponent(BaseIntegration): 

    def __init__(self, *args, **kwargs):
        super().__init__(integration_type="component", *args, **kwargs)