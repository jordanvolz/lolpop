from lolpop.component.resource_version_control.base_resource_version_control import BaseResourceVersionControl
from lolpop.utils import common_utils as utils
import os 
import joblib
import pandas as pd

# an assumption we make using this component is that dvc is already set up. 
# that is -- `dvc init --subdir` has been run on a subdir of the main git repo
# this is specified by the DVC_DIR variable. And a remote has been set up with 
# the id given in DVC_REMOTE 
@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class dvcVersionControl(BaseResourceVersionControl): 
    __REQUIRED_CONF__ = {
        "config" : ["DVC_DIR", "DVC_REMOTE"]
    }

    __DEFAULT_CONF__ = {
        "config": {"dvc_dir": "dvc/", "dvc_remote": "local"}
    }

    def __init__(self, *args, **kwargs): 
        #set normal config
        super().__init__(*args, **kwargs)
        
        secrets = utils.load_config(["DVC_DIR", "DVC_REMOTE"], 
                                    utils.copy_config_into(self.config,self.__DEFAULT_CONF__.get("config",{})))

        self.dvc_dir = secrets.get("DVC_DIR")
        if self.dvc_dir[-1] != "/":
            self.dvc_dir = self.dvc_dir + "/"
        self.dvc_remote = secrets.get("DVC_REMOTE")

        if self.dvc_remote == "local": 
            output, _ = utils.execute_cmd(["dvc",  "remote", "list"])
            if "local" not in output: 
                local_dir = "%s/dvc" %(self._get_config("local_dir"))
                self.log("Creating dvc remote 'local' for local directory %s" %local_dir)
                _ = utils.execute_cmd(["dvc", "remote", "add", "-d", "local",  local_dir])

        self.git_url = utils.execute_cmd(["git", "config", "--get", "remote.origin.url"], self)[0].strip()

    def version_data(self, dataset_version, data, key = None, **kwargs): 
        id = self.metadata_tracker.get_resource_id(dataset_version)

        #set up paths
        dvc_path = self.dvc_dir
        if key: 
            dvc_file = "%s_%s.csv" %(id, key)
        else: 
            dvc_file = "%s.csv" %(id)
        file_path = dvc_path + dvc_file
        
        #dump dataframe to dvc path
        data.to_csv(file_path, index=False)
        
        #commit file to dvc and .dvc file to git, and  then dvc push
        _,_ = utils.execute_cmd(["dvc", "add", file_path], self)
        _,_ = utils.execute_cmd(["dvc",  "commit", file_path], self)
        #git repo needs to have .dvc directory or else dvc doesn't know where to download from when using `dvc get`
        hexsha = utils.git_commit_file(".dvc/", msg="Committing .dvc directory", push=False, logger=self)
        hexsha = utils.git_commit_file("%s.dvc" %file_path, msg="Committing dvc file", logger=self)
        _,_ = utils.execute_cmd(["dvc", "push", "--remote", self.dvc_remote], self)
        #I don't think the URI is really needed. We should always access via dvc commands 
        URI, _ = utils.execute_cmd(["dvc", "get", os.getcwd(), file_path, "--show-url"], self)
        
        return {"uri" : URI, "hexsha": hexsha}

    def get_data(self, dataset_version, vc_info, key = None, **kwargs):
        if vc_info is not None: 
            hexsha = vc_info.get("hexsha")
        id = self.metadata_tracker.get_resource_id(dataset_version)
        if key:
            dvc_file = "%s_%s.csv" % (id, key)
        else:
            dvc_file = "%s.csv" % (id)

        file_path = self.dvc_dir + dvc_file 
        #if path exists, remove it before downloading. 
        if os.path.exists(dvc_file):
            os.remove(dvc_file)
        _, _ = utils.execute_cmd(["dvc", "get", self.git_url, file_path, "--rev", hexsha, "-o", dvc_file], self)
        df = pd.read_csv(dvc_file)
        
        return df 

    def version_model(self, experiment, model, algo, key=None, **kwargs): 
        id = self.metadata_tracker.get_resource_id(experiment)
        model_version_id = self.metadata_tracker.get_parent_id(experiment, type="experiment")
        if key:
            id = "%s_%s" % (id, key)

        # set up directories and dump model
        dvc_path = self.dvc_dir
        model_dir = dvc_path + "models/%s/%s" %(model_version_id, algo)    
        os.makedirs(model_dir, exist_ok=True)
        model_file = "models/%s/%s/%s" %(model_version_id, algo, id)
        model_path = dvc_path + model_file  
        joblib.dump(model, model_path)

        #now commit to dvc
        _,_ = utils.execute_cmd(["dvc", "add", model_path], self)
        _,_ = utils.execute_cmd(["dvc", "commit", model_path], self)
        hexsha = utils.git_commit_file(".dvc/", msg="Committing .dvc directory", push=False, logger=self)
        hexsha = utils.git_commit_file("%s.dvc" %model_path,msg="Committing dvc file", logger=self)
        _,_ = utils.execute_cmd(["dvc", "push", "--remote", self.dvc_remote], self)
        URI, _ = utils.execute_cmd(["dvc", "get", os.getcwd(), model_path, "--show-url"], self)

        return {"uri" : URI, "hexsha": hexsha}
  
    def get_model(self, experiment, key = None, **kwargs): 
        id = self.metadata_tracker.get_resource_id(experiment)
        if key:
            id = "%s_%s" % (id, key)
        model_version_id = self.metadata_tracker.get_parent_id(experiment, type="experiment")
        algo = self.metadata_tracker.get_metadata(experiment,id="model_trainer")
        hexsha = self.metadata_tracker.get_vc_info(experiment, key="hexsha").get("hexsha")
        dvc_file = "models/%s/%s/%s" %(model_version_id,algo,id)
        file_path = self.dvc_dir + dvc_file
        #if path exists, remove it before downloading.
        if os.path.exists(dvc_file):
            os.remove(dvc_file)
        _, _ = utils.execute_cmd(["dvc", "get", self.git_url, file_path,  "--rev", hexsha, "-o", dvc_file], self)
        model = joblib.load(dvc_file)
        return model

    