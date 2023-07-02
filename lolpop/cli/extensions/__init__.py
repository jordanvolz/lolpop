from pkgutil import extend_path

#allows extensions to work when doing local dev
__path__ = extend_path(__path__, __name__)

def __map_extensions__():
    import os
    from importlib import import_module
    import warnings

    warnings.filterwarnings("ignore")
    #get current directory and all subdirectors. These represent the resource types
    for path in __path__:
        subdirs = ["%s/%s" % (path, x) for x in os.listdir(path)
                if ((x[0] != "_") and (x[0] != ".") and (".py" not in x))]
        for subdir in subdirs:
            files = [x for x in os.listdir(subdir)
                    if ((x[0] != "_") and (x[0] != ".") and (".py" in x))]

            #from each file, import all classes and register them in the global namespace.
            for file in files:
                try:
                    subdir_arr = subdir.split("/")
                    file_name = file[:-3]
                    module = import_module(
                        "lolpop.cli.extensions.%s.%s" % (subdir_arr[-1],file_name))
                    globals().update({file_name: module})
                except Exception as e:
                    pass

    warnings.resetwarnings()
__map_extensions__()
