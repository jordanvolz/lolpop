from pkgutil import extend_path
import typer 

#allows extensions to work when doing local dev
__path__ = extend_path(__path__, __name__)

def __map_extensions__():
    from pathlib import Path
    import os
    from importlib import import_module
    from inspect import isclass
    import warnings

    warnings.filterwarnings("ignore")
    #get current directory and all subdirectors. These represent the resource types
    path = Path(__file__).parent.resolve()
    files = [x for x in os.listdir(path)
               if ((x[0] != "_") and (x[0] != ".") and (".py" in x))]

    #from each file, import all classes and register them in the global namespace.
    for file in files:
        try:
            module = import_module("lolpop.extension.cli.%s" % (file))
            commands = [x for x in dir(module) if isinstance(
                getattr(module, x), typer.main.Typer)]
            globals().update({name: getattr(module, name)
                                for name in commands})
        except:
            pass

    warnings.resetwarnings()
__map_extensions__()
