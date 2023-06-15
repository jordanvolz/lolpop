```
class ContinualVersionControl(BaseResourceVersionControl): 
    '''
    A class that facilitates version control of datasets and models in the Continual platform.

    Attributes
    ----------
    description : str, optional
        The description of the run. Defaults to None.
    run_id : str, optional
        The id of the run. Defaults to None.
    components : dict, optional
        The dictionary of components used for metadata tracking. Defaults to an empty dictionary.

    Methods
    -------
    version_data(dataset_version, data, key="data_csv", **kwargs)
        Method that versions the given dataset to a Continual resource.
        
        Parameters
        ----------
        dataset_version : str
            The dataset version you want to version.
        data : pandas.core.frame.DataFrame
            The dataset to version.
        key : str, optional
            The key to identify the dataset. Defaults to "data_csv".
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        dict
            A dictionary containing the URI of the artifact of the dataset.

    get_data(dataset_version, vc_info=None, key="data_csv", **kwargs)
        Method that retrieves the dataset from a Continual resource.
        
        Parameters
        ----------
        dataset_version : str
            The dataset version you want to retrieve.
        vc_info : None, optional
            Information about the version control. Default to None.
        key : str, optional
            The key to identify the artifact. Defaults to "data_csv".
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        pandas.core.frame.DataFrame
            The retrieved dataset from the Continual platform.

    version_model(experiment, model, algo, **kwargs)
        Method that versions the given model to a Continual resource.
        
        Parameters
        ----------
        experiment : str
            The experiment version you want to version.
        model : any
            The model to version.
        algo : str
            The algorithm name used for the versioning.
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        dict
            A dictionary containing the URI of the artifact of the model.

    get_model(experiment, key="model_artifact", **kwargs)
        Method that retrieves the model from a Continual resource.
        
        Parameters
        ----------
        experiment : str
            The experiment version you want to retrieve.
        key : str, optional
            The key to identify the model artifact. Defaults to "model_artifact".
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        any
            The retrieved model from the Continual platform.
    '''
    
    __REQUIRED_CONF__ = {
        "config" : ["local_dir"]
    }
    def __init__(self, description=None, run_id=None, components={}, *args, **kwargs): 
        '''
        The class constructor.
        
        Parameters
        ----------
        description : str, optional
            The description of the run. Defaults to None.
        run_id : str, optional
            The id of the run. Defaults to None.
        components : dict, optional
            The dictionary of components used for metadata tracking. Defaults to an empty dictionary.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        '''

        #set normal config
        super().__init__(components=components, *args, **kwargs)
        
        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case. 
        if isinstance(components.get("metadata_tracker"), ContinualMetadataTracker): 
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else: 
            secrets = utils.load_config(["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"], self.config)
            self.client = cutils.get_client(secrets)
            self.run = cutils.get_run(self.client, description=description, run_id=run_id)

    def version_data(self, dataset_version, data, key="data_csv", **kwargs): 
        '''
        Method that versions the given dataset to a Continual resource.

        Parameters
        ----------
        dataset_version : str
            The dataset version you want to version.
        data : pandas.core.frame.DataFrame
            The dataset to version.
        key : str, optional
            The key to identify the dataset. Defaults to "data_csv".
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        dict
            A dictionary containing the URI of the artifact of the dataset.
        '''
        id = self.metadata_tracker.get_resource_id(dataset_version)

        #dump dataframe to local
        local_path = "%s/%s.csv" %(self.config.get("local_dir"),id)
        data.to_csv(local_path, index=False)

        artifact = self.metadata_tracker.log_artifact(dataset_version, id = key, path = local_path, mime_type="csv", external=False)
        
        return {"uri" : artifact.url}

    def get_data(self, dataset_version, vc_info=None, key="data_csv", **kwargs):
        '''
        Method that retrieves the dataset from a Continual resource.

        Parameters
        ----------
        dataset_version : str
            The dataset version you want to retrieve.
        vc_info : None, optional
            Information about the version control. Default to None.
        key : str, optional
            The key to identify the artifact. Defaults to "data_csv".
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        pandas.core.frame.DataFrame
            The retrieved dataset from the Continual platform.
        '''
        artifact = dataset_version.artifacts.get(id=key)
        file_path = "%s/%s/%s" %(self._get_config("local_dir"),dataset_version.id, artifact.id)
        os.makedirs(file_path, exist_ok=True)
        _, download_path = artifact.download(dest_dir=file_path)
        df = pd.read_csv(download_path)
        return df

    def version_model(self, experiment, model, algo, **kwargs): 
        '''
        Method that versions the given model to a Continual resource.

        Parameters
        ----------
        experiment : str
            The experiment version you want to version.
        model : any
            The model to version.
        algo : str
            The algorithm name used for the versioning.
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        dict
            A dictionary containing the URI of the artifact of the model.
        '''
        id = self.metadata_tracker.get_resource_id(experiment)

        model_dir = "%s/models/%s" %(self._get_config("local_dir"), algo)    
        os.makedirs(model_dir, exist_ok=True)
        model_path = "%s/%s" %(model_dir, id)
        joblib.dump(model, model_path)
        artifact = self.metadata_tracker.log_artifact(experiment, id = "model_artifact", path=model_path, external=False)

        return {"uri" : artifact.url}
    
    def get_model(self, experiment, key="model_artifact", **kwargs): 
        '''
        Method that retrieves the model from a Continual resource.

        Parameters
        ----------
        experiment : str
            The experiment version you want to retrieve.
        key : str, optional
            The key to identify the model artifact. Defaults to "model_artifact".
        **kwargs : dict
            Additional key-value arguments.

        Returns
        -------
        any
            The retrieved model from the Continual platform.
        '''
        artifact = self.metadata_tracker.get_artifact(experiment,id=key)
        file_path = "%s/%s" %(self._get_config("local_dir"),experiment.id)
        os.makedirs(file_path, exist_ok=True)
        _, download_path = artifact.download(dest_dir=file_path)
        model = joblib.load(download_path)
        
        return model
```