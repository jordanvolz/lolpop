def __map_extensions__():
    from pathlib import Path
    import os
    from importlib import import_module
    from inspect import isclass
    from lolpop.component.base_component import BaseComponent
    from lolpop.pipeline.base_pipeline import BasePipeline
    from lolpop.runner.base_runner import BaseRunner
    import warnings

    warnings.filterwarnings("ignore")
    #get current directory and all subdirectors. These represent the extensions 
    # resource types
    path = Path(__file__).parent.resolve() #lolpop/extension
    extensions = ["%s/%s" % (path, x) for x in os.listdir(path)
                  if ((x[0] != "_") and (x[0] != ".") and (".py" not in x))]
    #iterate through extensions and add each top level 
    for extension in extensions: #lolpop/extension/my_extension
        resources = ["%s/%s" % (extension, x) for x in os.listdir(extension)
                     if ((x[0] != "_") and (x[0] != ".") and (".py" not in x))]
        for resource in resources: #lolpop/extension/my_extension/{component,pipeline,runner}
            subdirs = ["%s/%s" % (resource, x) for x in os.listdir(resource)
                       if ((x[0] != "_") and (x[0] != ".") and (".py" not in x))]
        #for each resource type (i.e. subdir), get all resources implemented in that type (i.e. python files in the subdir)
        for subdir in subdirs:
            files = [x for x in os.listdir(subdir) if (
                (".py" in x) and ("__" not in x) and (x[0] != "."))]
            #from each file, import all classes and register them in the global namespace.
            for file in files:
                subdir_arr = subdir.split("/")
                module = import_module("lolpop.extension.%s.%s.%s.%s" % (
                    subdir_arr[-3], subdir_arr[-2], subdir_arr[-1], file[:-3]))
                classes = [x for x in dir(module) if isclass(getattr(module, x))]
                components = [x for x in classes if (
                    issubclass(getattr(module, x), BaseComponent)
                    or issubclass(getattr(module, x), BasePipeline)
                    or issubclass(getattr(module, x), BaseRunner)
                    )]
                globals().update({name: getattr(module, name)
                                for name in components})

        warnings.resetwarnings()


__map_extensions__()
