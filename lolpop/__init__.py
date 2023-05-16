
def __get_template_dir__(): 
    import os 

    LOLPOP_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMPLATE_DIR = LOLPOP_DIR + "/templates"

    return TEMPLATE_DIR

__template_path__ = __get_template_dir__()