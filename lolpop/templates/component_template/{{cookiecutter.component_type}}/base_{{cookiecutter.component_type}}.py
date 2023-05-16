from lolpop.component import BaseComponent


class Base{{cookiecutter.ComponentType}}(BaseComponent):
    #Add required configuration here
    __REQUIRED_CONF__ = {
        "config": []
    }

    #Add default configuration here 
    __DEFAULT_CONF__ = {
        "config": {}
    }

    def __init__(self, conf, pipeline_conf, runner_conf, **kwargs):
        self.__file_path__ = __file__
        #set normal config
        super().__init__(conf, pipeline_conf, runner_conf, **kwargs)

    # Write your functions here. The Base Class should primarily just implement an interface for 
    # other classes to implement.   
    def my_function(self, required_arg1, required_arg2, *args, **kwargs):
        pass

    def my_other_function(self, required_arg1, required_arg2, *args, **kwargs):
        pass
