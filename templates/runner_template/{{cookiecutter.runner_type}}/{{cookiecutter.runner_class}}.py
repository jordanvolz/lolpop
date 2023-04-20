from .base_{{cookiecutter.runner_type}} import Base{{cookiecutter.RunnerType}}
from lolpop.utils import common_utils as utils
#import your libraries here

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class {{cookiecutter.RunnerClass}}(Base{{cookiecutter.RunnerType}}):
    #Override required or default configurations here for your class
    ##Add required configuration here
    #__REQUIRED_CONF__ = {
    #    "config": []
    #}
    ##Add default configuration here
    #__DEFAULT_CONF__ = {
    #    "config": {}
    #}

    def __init__(self, conf, **kwargs):
        #set normal config
        super().__init__(conf, **kwargs)
        #Add any additional class initialization code here.

    # Write your functions here. Implement Base class functions and actually write them! 
    def my_function(self, required_arg1, required_arg2, *args, **kwargs):
        #Your code goes here!
        pass

    def my_other_function(self, required_arg1, required_arg2, *args, **kwargs):
        #Your code goes here!
        pass
