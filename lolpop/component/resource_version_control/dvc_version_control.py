from lolpop.component.resource_version_control.abstract_resource_version_control import AbstractResourceVersionControl
from lolpop.utils import common_utils as utils

# an assumption we make using this component is that dvc is already set up. 
# that is -- `dvc init --subdir` has been run on a subdir of the main git repo
# this is specified by the DVC_DIR variable. And a remote has been set up with 
# the id given in DVC_REMOTE 
@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class dvcVersionControl(AbstractResourceVersionControl): 
    __REQUIRED_CONF__ = {
        "config" : ["DVC_DIR", "DVC_REMOTE"]
    }

    def __init__(self, conf, pipeline_conf, runner_conf, description=None, run_id=None, **kwargs): 
        #set normal config
        super().__init__(conf, pipeline_conf, runner_conf, **kwargs)
        
        secrets = utils.load_config(["DVC_DIR", "DVC_REMOTE"], conf)
        self.dvc_dir = secrets.get("DVC_DIR")
        self.dvc_remote = secrets.get("DVC_REMOTE")

    def version_data(self, dataset_version, data, file_suffix = None, **kwargs): 
        id = self.metadata_tracker.get_resource_id(dataset_version)

        #set up paths
        dvc_path = self.dvc_dir
        if file_suffix: 
            dvc_file = "%s_%s.csv" %(id, file_suffix)
        else: 
            dvc_file = "%s.csv" %(id)
        file_path = "%s/%s" %(dvc_path, dvc_file)
        
        #dump dataframe to dvc path
        data.to_csv(file_path, index=False)
        
        #commit file to dvc and .dvc file to git, and  then dvc push
        _,_ = utils.execute_cmd("dvc add %s" %file_path)
        _,_ = utils.execute_cmd("dvc commit %s/*" %dvc_path)
        hexsha = utils.git_commit_file("%s.dvc" %file_path, msg="Committing dvc file")
        _,_ = utils.execute_cmd("dvc push --remote %s" %self.dvc_remote)
        #I don't think the URI is really needed. We should always access via dvc commands 
        URI,_ = utils.execute_cmd("dvc get %s --show-url" %(os.getcwd(), file_path))
        
        return {"uri" : URI, "hexsha": hexsha}

    def get_data(self, dataset_version, vc_info, **kwargs):
        if vc_info is not None: 
            hexsha = vc_info.get("hexsha")
        id = self.metadata_tracker.get_resource_id(dataset_version)
        dvc_file = "%s.csv" %(id)
    
        _,_ = execute_cmd("dvc get %s %s/%s --rev %s -o %s" %(os.getcwd(), self.dvc_dir, dvc_file, hexsha, dvc_file))
        df = pd.read_csv(dvc_file)
        
        return df 

    def version_model(self, experiment, model, algo, **kwargs): 
        id = self.metadata_tracker.get_resource_id(experiment)
        model_version_id = self.metadata_tracker.get_parent_id(experiment,)

        # set up directories and dump model
        dvc_path = self.dvc_dir
        model_dir = "%s/models/%s/%s" %(dvc_path, model_version_id, algo)    
        os.makedirs(model_dir, exist_ok=True)
        model_file = "models/%s/%s/%s" %(model_version_id, algo, id)
        model_path = "%s/%s" %(dvc_path, model_file)  
        joblib.dump(model, model_path)

        #now commit to dvc
        _,_ = execute_cmd("dvc add %s" %model_path)
        _,_ = execute_cmd("dvc commit %s/*" %dvc_path)
        hexsha = utils.git_commit_file("%s.dvc" %model_path,msg="Committing dvc file")
        _,_ = execute_cmd("dvc push --remote %s" %self._get_config("DVC_REMOTE"))
        URI,_ = execute_cmd("dvc get %s %s --show-url" %(os.getcwd(), model_path))

        return {"uri" : URI, "hexsha": hexsha}
  
    def get_model(self, experiment, **kwargs): 
        id = self.metadata_tracker.get_resource_id(experiment)
        model_version_id = self.metadata_tracker.get_parent_id(experiment)
        algo = self.metadata_tracker.get_metadata(experiment,key="model_trainer")
        hexsha = self.metadata_tracker.get_metadata(experiment, key="git_hexsha").get("hexsha")
        dvc_file = "model/%s/%s/%s" %(model_version_id,algo,id)
        _,_ = execute_cmd("dvc get %s %s/%s --rev %s -o %s" %(os.getcwd(), self.dvc_dir, dvc_file, hexsha, dvc_file))
        model = joblib.load(dvc_file)
        return model

    