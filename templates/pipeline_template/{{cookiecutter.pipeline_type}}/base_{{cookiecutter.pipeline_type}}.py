from lolpop.pipeline.base_pipeline import BasePipeline


class Base{{cookiecutter.PipelineType}}(BasePipeline):
    #Add required configuration here
    __REQUIRED_CONF__ = {
        "config": []
    }

    #Add default configuration here 
    __DEFAULT_CONF__ = {
        "config": {}
    }

    # Write your functions here. The Base Class should primarily just implement an interface for 
    # other classes to implement.   
    def my_function(self, required_arg1, required_arg2, *args, **kwargs):
        pass

    def my_other_function(self, required_arg1, required_arg2, *args, **kwargs):
        pass
