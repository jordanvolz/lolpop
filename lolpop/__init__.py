
from pkgutil import extend_path

#allows extensions to work when doing local dev and adding them to sys path
__path__ = extend_path(__path__, __name__)

def __get_template_dir__(): 
    import os 

    LOLPOP_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMPLATE_DIR = LOLPOP_DIR + "/templates"

    return TEMPLATE_DIR

def __suppress_warnings__(): 
    import os 

    #deepchecks
    os.environ["DISABLE_LATEST_VERSION_CHECK"]="True"
    #alibi
    os.environ["TF_CPP_MIN_LOG_LEVEL"]="1"

__template_path__ = __get_template_dir__()
__suppress_warnings__()