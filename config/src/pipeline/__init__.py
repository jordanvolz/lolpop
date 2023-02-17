# from .train.abstract_train import AbstractTrain
# from .process.abstract_process import AbstractProcess
# from .predict.abstract_predict import AbstractPredict

# from .process.classification_process import ClassificationProcess

#instead of manually adding classes, let's try to load them all dynamically
# folder structure is resource/resource_type/resource_name.py
# like components/data_transformer/dbt_data_transformer.py
# in each class we want to load class top level so they can be accessed via resource.Class
# such as components.dbtDataTransformer
from pathlib import Path
import os 

#get current directory and all subdirectors. These represent the resource types
path = Path(__file__).parent.resolve()
subdirs = ["%s/%s" %(path,x) for x in os.listdir(path) if ((x[0] != "_") and (".py" not in x) )]
#for each resource type (i.e. subdir), get all resources implemented in that type (i.e. python files in the subdir)
for subdir in subdirs: 
    files = [ x for x in os.listdir(subdir) if ((".py" in x) and ("__" not in x))]
    #from each file, import all classes and register them in the global namespace. 
    for file in files: 
        module = __import__("%s.%s.%s" %(subdir.split("/")[-2],subdir.split("/")[-1],file[:-3]), fromlist=["*"])
        classes = [x for x in dir(module) if not x.startswith("_")]
        globals().update({name: getattr(module,name) for name in classes})