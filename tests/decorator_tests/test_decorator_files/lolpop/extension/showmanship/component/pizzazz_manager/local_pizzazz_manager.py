from lolpop.component import BaseComponent
from lolpop.utils import common_utils as utils
from functools import wraps

@utils.decorate_all_methods([utils.error_handler])
class LocalPizzazzManager(BaseComponent):

    __DEFAULT_CONF__ = {
        "config": {
                   "decorator_method": "pizzazz_decorator",
                }
    }

    def pizzazz_decorator(self, func, cls): 
            @wraps(func)
            def wrapper(*args, **kwargs):
                return "You're at your best when when the going gets rough. You've been put to the test, but it's never enough. You got the touch! You got the power! When all hell's breaking loose you'll be riding the eye of the storm. You got the heart! You got the motion! You know that when things get too tough, you got the touch!"

            return wrapper