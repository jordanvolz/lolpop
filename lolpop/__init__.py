#it's nice to be able to walk the directory structure, but this makes the lolpop load time slow 
#from . import component, pipeline, runner, utils

def __get_template_dir__(): 
    import os 

    LOLPOP_DIR = os.path.dirname(os.path.realpath(__file__))
    PARENT_DIR = os.path.dirname(LOLPOP_DIR)
    TEMPLATE_DIR = PARENT_DIR + "/templates"

    return TEMPLATE_DIR

__template_path__ = __get_template_dir__()