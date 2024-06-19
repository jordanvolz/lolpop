from lolpop.component.base_component import BaseComponent
from lolpop.utils import common_utils as utils
from typing import Any


class BaseVectorStore(BaseComponent):
    __REQUIRED_CONF__ = {
        "component": [""],
        "config": ["embedding"],
    }

