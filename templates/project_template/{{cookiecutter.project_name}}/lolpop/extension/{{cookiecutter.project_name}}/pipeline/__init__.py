
def __map_pipelines__():
    from pathlib import Path
    import os
    from importlib import import_module
    from inspect import isclass
    from lolpop.pipeline import BasePipeline
    import warnings

    warnings.filterwarnings("ignore")
    #get current directory and all subdirectors. These represent the resource types
    path = Path(__file__).parent.resolve()
    subdirs = ["%s/%s" % (path, x) for x in os.listdir(path)
               if ((x[0] != "_") and (x[0] != ".") and (".py" not in x))]
    #for each resource type (i.e. subdir), get all resources implemented in that type (i.e. python files in the subdir)
    for subdir in subdirs:
        files = [x for x in os.listdir(subdir) if (
            (".py" in x) and (x[0] != ".") and ("__" not in x))]
        #from each file, import all classes and register them in the global namespace.
        for file in files:
            module = import_module("lolpop.extension.{{cookiecutter.project_name}}.%s.%s.%s" % (
                subdir.split("/")[-2], subdir.split("/")[-1], file[:-3]))
            classes = [x for x in dir(module) if isclass(getattr(module, x))]
            pipelines = [x for x in classes if issubclass(
                getattr(module, x), BasePipeline)]
            globals().update({name: getattr(module, name)
                              for name in pipelines})

    warnings.resetwarnings()


__map_pipelines__()
