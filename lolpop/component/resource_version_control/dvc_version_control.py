from lolpop.component.resource_version_control.base_resource_version_control import BaseResourceVersionControl
from lolpop.utils import common_utils as utils
from pathlib import Path 
import os 
import joblib
import pandas as pd

# an assumption we make using this component is that dvc is already set up. 
# that is -- `dvc init --subdir` has been run on a subdir of the main git repo
# this is specified by the DVC_DIR variable. And a remote has been set up with 
# the id given in DVC_REMOTE 
@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class dvcVersionControl(BaseResourceVersionControl): 

    __DEFAULT_CONF__ = {
        "config": {"dvc_dir": "dvc/", 
                   "dvc_remote": "local", 
                   "disable_git_commit": False, 
                   "disable_git_push": False, 
                   "git_path_to_dvc_dir": None, 
                   }
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
        
        if not self._get_config("disable_git_commit"): 
            #make sure the .dvc/config file is comitted. 
            utils.git_commit_file(".dvc/config", 
                                msg="Committing .dvc/config", 
                                push=False, 
                                path_from_root=self._get_config("git_path_to_dvc_dir"),
                                logger=self)

    def version_data(self, dataset_version, data, key = None, *args, **kwargs): 
        """
        Version the input dataset using dvc (Data Version Control) and output information about the versioned dataset 
        including versioning id and URI.
        
        Args: 
        dataset_version: str, ID of the dataset being versioned.
        data: DataFrame, the dataset to version.
        key: str, optional, default: None, a unique identifier for the dataset version. 
        
        Returns:
        dictionary containing dataset versioning information including the URI and hexsha.
                
        """
        id = self.metadata_tracker.get_resource_id(dataset_version)

        #set up paths
        dvc_path = self.dvc_dir
        data_dir = "%s/data" %dvc_path 
        os.makedirs(data_dir, exist_ok=True)
        if key: 
            dvc_file = "data/%s_%s.csv" %(id, key)
        else: 
            dvc_file = "data/%s.csv" %(id)
        file_path = dvc_path + dvc_file
        
        #dump dataframe to dvc path
        data.to_csv(file_path, index=False)
        
        #commit file to dvc and .dvc file to git, and  then dvc push
        _,_ = utils.execute_cmd(["dvc", "add", file_path], self)
        _,_ = utils.execute_cmd(["dvc",  "commit", file_path], self)
        #git repo needs to have .dvc/config or else dvc doesn't know where to download from when using `dvc get`
        hexsha=None
        if not self._get_config("disable_git_commit"):
            git_push = not self._get_config("disable_git_push")
            hexsha = utils.git_commit_file("%s.dvc" % file_path, 
                                           msg="Committing dvc file", 
                                           push=git_push, 
                                           path_from_root=self._get_config("git_path_to_dvc_dir"),
                                           logger=self)
        _,_ = utils.execute_cmd(["dvc", "push", "--remote", self.dvc_remote], self)
        #I don't think the URI is really needed. We should always access via dvc commands 
        URI, _ = utils.execute_cmd(["dvc", "get", os.getcwd(), file_path, "--show-url"], self)
        
        return {"uri" : URI, "hexsha": hexsha}

    def get_data(self, dataset_version, vc_info=None, key = None, *args, **kwargs):
        """
        Get the versioned dataset from dvc (Data Version Control) using information about the dataset version.

        Args:
        dataset_version: str, ID of the dataset version to retrieve.
        vc_info: dictionary, containing versioning information for the dataset.
        key: str, optional, default: None, a unique identifier for the dataset version.

        Returns:
        DataFrame containing the versioned dataset.

        """
        if vc_info is None: 
            vc_info = self.metadata_tracker.get_vc_info(dataset_version)
        hexsha = vc_info.get("hexsha")
        df = pd.DataFrame()
        if hexsha is not None and hexsha != 'None': 
            id = self.metadata_tracker.get_resource_id(dataset_version)
            if key:
                dvc_file = "data/%s_%s.csv" % (id, key)
            else:
                dvc_file = "data/%s.csv" % (id)

            file_path = self.dvc_dir + dvc_file 
            if self._get_config("git_path_to_dvc_dir") is not None: 
                file_path = str(Path(self._get_config("git_path_to_dvc_dir")) / file_path)
            #if path exists, remove it before downloading. 
            if os.path.exists(dvc_file):
                os.remove(dvc_file)
            _, _ = utils.execute_cmd(["dvc", "get", self.git_url, file_path, "--rev", hexsha, "-o", dvc_file], self)
            df = pd.read_csv(dvc_file)
            
        return df 

    def version_model(self, experiment, model, algo=None, key=None, *args, **kwargs): 
        """
        Version the input model using dvc (Data Version Control) and output information about the versioned model 
        including versioning id and URI.
        
        Args: 
        experiment: str, unique ID of the experiment.
        model: object, the model to version.
        algo: string, the algorithm used to train the model.
        key: str, optional, default:None, a unique identifier for the model version. 
        
        Returns:
        dictionary containing model versioning information including the URI and hexsha.
        
        """
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
        hexsha=None
        if not self._get_config("disable_git_commit"): 
            git_push = not self._get_config("disable_git_push")
            hexsha = utils.git_commit_file("%s.dvc" % model_path, 
                                           msg="Committing dvc file", 
                                           push = git_push,
                                           path_from_root=self._get_config("git_path_to_dvc_dir"), 
                                           logger=self)
        _,_ = utils.execute_cmd(["dvc", "push", "--remote", self.dvc_remote], self)
        URI, _ = utils.execute_cmd(["dvc", "get", os.getcwd(), model_path, "--show-url"], self)

        return {"uri" : URI, "hexsha": hexsha}
  
    def get_model(self, experiment, key = None, *args, **kwargs): 
        """
        Get the versioned model using versioning information about the model.

        Args:
        experiment: str, unique ID of the experiment.
        key: str, optional, default: None, a unique identifier for the model version.

        Returns:
        the versioned model.

        """
        id = self.metadata_tracker.get_resource_id(experiment)
        if key:
            id = "%s_%s" % (id, key)
        model_version_id = self.metadata_tracker.get_parent_id(experiment, type="experiment")
        algo = self.metadata_tracker.get_metadata(experiment,id="model_trainer")
        hexsha = self.metadata_tracker.get_vc_info(experiment, key="hexsha").get("hexsha")
        model = None
        if hexsha is not None and hexsha != 'None':    
            dvc_file = "models/%s/%s/%s" %(model_version_id,algo,id)
            file_path = self.dvc_dir + dvc_file
            if self._get_config("git_path_to_dvc_dir") is not None:
                file_path = str(Path(self._get_config("git_path_to_dvc_dir")) / file_path)
            #if path exists, remove it before downloading.
            if os.path.exists(dvc_file):
                os.remove(dvc_file)
            _, _ = utils.execute_cmd(["dvc", "get", self.git_url, file_path,  "--rev", hexsha, "-o", dvc_file], self)
            model = joblib.load(dvc_file)
        return model

    def version_feature_transformer(self, experiment, transformer, transformer_class=None, key=None, *args, **kwargs):
        """
        Version the input feature transformer using dvc (Data Version Control) and output 
        information about the versioned transformer including versioning id and URI.
        
        Args: 
        experiment: str, unique ID of the experiment.
        transformer: object, the transform to version.
        transform_class: string, the feature transform class
        key: str, optional, default:None, a unique identifier for the transform version 
        
        Returns:
        dictionary containing transform versioning information including the URI and hexsha.
        
        """
        id = self.metadata_tracker.get_resource_id(experiment)
        model_version_id = self.metadata_tracker.get_parent_id(experiment, type="experiment")
        if key:
            id = "%s_%s" % (id, key)

        # set up directories and dump model
        dvc_path = self.dvc_dir
        transformer_dir = dvc_path + "transformers/%s/%s" % (model_version_id, transformer_class)
        os.makedirs(transformer_dir, exist_ok=True)
        transformer_file = "transformers/%s/%s/%s" % (model_version_id, transformer_class, id)
        transformer_path = dvc_path + transformer_file
        joblib.dump(transformer, transformer_path)

        #now commit to dvc
        _, _ = utils.execute_cmd(["dvc", "add", transformer_path], self)
        _, _ = utils.execute_cmd(["dvc", "commit", transformer_path], self)
        hexsha = None
        if not self._get_config("disable_git_commit"):
            git_push = not self._get_config("disable_git_push")
            hexsha = utils.git_commit_file("%s.dvc" % transformer_path,
                                           msg="Committing dvc file",
                                           push=git_push,
                                           path_from_root=self._get_config("git_path_to_dvc_dir"),
                                           logger=self)
        _, _ = utils.execute_cmd(["dvc", "push", "--remote", self.dvc_remote], self)
        URI, _ = utils.execute_cmd(["dvc", "get", os.getcwd(), transformer_path, "--show-url"], self)

        return {"uri": URI, "hexsha": hexsha}

    def get_feature_transformer(self, experiment, key=None, *args, **kwargs):
        """
        Get the versioned feature transformer using versioning information.

        Args:
        experiment: str, unique ID of the experiment.
        key: str, optional, default: None, a unique identifier for the model version.

        Returns:
        the versioned model.

        """
        id = self.metadata_tracker.get_resource_id(experiment)
        if key:
            id = "%s_%s" % (id, key)
        model_version_id = self.metadata_tracker.get_parent_id(experiment, type="experiment")
        transformer_class = self.metadata_tracker.get_metadata(experiment, id="feature_transformer_class")
        hexsha = self.metadata_tracker.get_vc_info(experiment, key="feature_transformer_hexsha").get("hexsha")
        transformer = None
        if hexsha is not None and hexsha != 'None' and transformer_class is not None:
            dvc_file = "transformers/%s/%s/%s" % (model_version_id, transformer_class, id)
            file_path = self.dvc_dir + dvc_file
            if self._get_config("git_path_to_dvc_dir") is not None:
                file_path = str(Path(self._get_config("git_path_to_dvc_dir")) / file_path)
            #if path exists, remove it before downloading.
            if os.path.exists(dvc_file):
                os.remove(dvc_file)
            _, _ = utils.execute_cmd(
                ["dvc", "get", self.git_url, file_path,  "--rev", hexsha, "-o", dvc_file], self)
            transformer = joblib.load(dvc_file)
        return transformer

    