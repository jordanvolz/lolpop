from lolpop.runner import BaseRunner


class Base{{cookiecutter.RunnerType}}(BaseRunner):
    #Add required configuration here
    __REQUIRED_CONF__ = {
        "config": []
    }

    #Add default configuration here 
    __DEFAULT_CONF__ = {
        "config": {}
    }

    def __init__(self, conf, **kwargs):
        #set normal config
        self.__file_path__ == __file__
        super().__init__(conf, **kwargs)
        #Add any additional class initialization code here.

    # Write your functions here. The Base Class should primarily just implement an interface for 
    # other classes to implement.   
    def my_function(self, required_arg1, required_arg2, *args, **kwargs):
        pass

    def my_other_function(self, required_arg1, required_arg2, *args, **kwargs):
        pass
