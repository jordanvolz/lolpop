from lolpop.utils import common_utils as utils
from lolpop.base_integration import BaseIntegration

class BaseRunner(BaseIntegration):

    def __init__(self, *args, **kwargs):
        super().__init__(integration_type="runner", *args, **kwargs)
