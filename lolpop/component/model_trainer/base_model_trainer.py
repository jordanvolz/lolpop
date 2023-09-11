from lolpop.component.base_component import BaseComponent
from lolpop.utils import common_utils as utils 

from sklearn import metrics as sk_metrics
import pandas as pd 
import numpy as np 
from typing import Any 

class BaseModelTrainer(BaseComponent): 

    __REQUIRED_CONF__ = {
        "components" : ["metadata_tracker", "resource_version_control"], 
    }

    model = None 
    mlflow_module = "you_need_to_implement_this_for_mlflow_use"
    
    #predictions = {}
    def __init__(self, params=None, *args, **kwargs): 
        #set normal config
        super().__init__(params=params, *args, **kwargs)
        #if params aren't passed in, try to retrieve from config
        if params is None or params == {}: 
            params = self._get_config("training_params", {})
        self.params = params

        #load transformer if it has one
        transformer_class = self._get_config("transformer_class")
        if transformer_class is not None: 
            transformer_config = self.get_config("transformer_config")
            transformer_cl = utils.load_class(transformer_class)
            dependent_components = {"logger": self.logger, "notifier": self.notifier,  
                                    "metadata_tracker": self.metadata_tracker,
                                    "resource_version_control": self.resource_version_control}
            self.feature_transformer = transformer_cl(conf=transformer_config, pipeline_conf=self.pipeline_conf, runner_conf=self.runner_conf,
                         parent_process=self.name, problem_type=self.problem_type, components=dependent_components)
        

    def fit(self, data, *args, **kwargs) -> Any: 
        pass 

    def predict(self, data, *args, **kwargs) -> Any:
        pass

    def predict_df(self, df, *args, **kwargs) -> Any:
        pass

    def predict_proba_df(self, df, *args, **kwargs) -> Any:
        pass

    def get_artifacts(self, id, *args, **kwargs) -> dict[str, Any]:
        pass

    def transform_and_fit(self, data_dict, *args, **kwargs) -> Any: 
        #fit feature transformer
        self.fit_data(data_dict["X_train"], data_dict["y_train"])

        #transform features 
        transformed_data_dict = self._transform_dict(data_dict)

        #finally, fit model
        return self.fit(transformed_data_dict, *args, **kwargs)
    
    def transform_and_predict(self, data, *args, **kwargs) -> Any: 
        #transform data 
        transformed_data = self._transform_dict(data)
        
        #finally, call predict on transformed data         
        return self.predict(transformed_data, *args, **kwargs)
    
    def transform_and_predict_df(self, data, *args, **kwargs) -> Any: 
        #transform dataframe
        transformed_data = self.transform_data(data)

        #get predictions
        return self.predict_df(transformed_data, *args, **kwargs)

    def transform_and_predict_proba_df(self, data, *args, **kwargs) -> Any: 
        #transform dataframe
        transformed_data = self.transform_data(data)

        #get prediction probabilities
        return self.predict_proba_df(transformed_data, *args, **kwargs)

    def fit_transform_data(self, X_data, y_data, *args, **kwargs) -> Any:
        #fit data 
        self.fit_data(X_data, y_data)

        #transform data 
        data_out = self.transform_data(X_data)
        return data_out
        
    def fit_data(self, X_data, y_data=None, *args, **kwargs) -> Any:

        if hasattr(self, "feature_transformer"):
            self.log(
                "Fitting feature transformer on data for trainer %s." % self.name)
            self.feature_transformer.fit(X_data, y_data)
            return self.feature_transformer
        else:
            self.log("No feature transformer found for trainer %s." %
                     self.name)
            return None 

    def _transform_dict(self, data, *args, **kwargs) -> dict[Any]: 
        data_dict = data.copy() 

        #data is a dict of train/vali/test so we need to transform all X_ datasets
        for key in data_dict.keys():
            if key.startswith("X_"):
                data_dict[key] = self.transform_data(data_dict[key])

        return data_dict

    def transform_data(self, data, *args, **kwargs) -> Any: 
        data_out = data.copy() 

        if hasattr(self, "feature_transformer"):
            self.log("Running feature transformer on data for trainer %s." %self.name)
            data_out = self.feature_transformer.transform(data_out)
        else: 
            self.log("No feature transformer found for trainer %s." %self.name)

        return data_out


    def save(self, experiment, *args, **kwargs): 
        """Save the model.

        Args:
            experiment (object): experiment to save model into
        """
        algo = type(self).__name__
        vc_info = self.resource_version_control.version_model(experiment, self.model, algo=algo)
        experiment_metadata = {
            "training_params" : self.params,
            "model_trainer" : algo
        }
        self.metadata_tracker.register_vc_resource(experiment, vc_info, additional_metadata = experiment_metadata)

        if hasattr(self, "feature_transformer"): 
            self.feature_transformer.save(experiment)

        experiment_id = self.metadata_tracker.get_resource_id(experiment, type="experiment")
        model_artifacts = self.get_artifacts(experiment_id) or {}
        for k, v in model_artifacts.items():
            self.metadata_tracker.log_artifact(experiment, k, v)

    def load(self, *args, **kwargs) -> Any: 
        #load feature transformer
        pass 

    def _get_model(self, *args, **kwargs) -> Any:
        return self.model 
    
    #used to set model object. 
    def _set_model(self, model, *args, **kwargs): 
        self.model = model 
    #def _get_predictions(self): 
    #    return self.predictions

    def _get_transformer(self, *args, **kwargs) -> Any: 
        return self.feature_transformer
    
    def _set_transformer(self, transformer, *args, **kwargs): 
        self.feature_transformer = transformer

    def calculate_metrics(self, data, predictions, metrics, *args, **kwargs) -> dict[str, float]: 
        """Calculates metrics on the trained model. 

        Args:
            data (dict): dictonary of train/test/validation data 
            predictions (object): 
            metrics (list): list of metrics to calculate

        Returns:
            metrics_out: dictionary of computed metrics
        """
        metrics_out = {"train" : {}, "valid" : {}, "test" : {}}

        test_exists = data.get("y_test") is not None
        valid_exists = data.get("y_valid") is not None

        if self.problem_type == "classification": 
            multi_class = False
            average="binary"
            num_classes = len(data["y_train"].unique())
            if num_classes > 2: 
                multi_class = True 
                average = "weighted"

        for metric in metrics: 
            if metric == "accuracy": 
                metrics_out["train"][metric] = sk_metrics.accuracy_score(data["y_train"], predictions["train"])
                if valid_exists: 
                    metrics_out["valid"][metric] = sk_metrics.accuracy_score(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.accuracy_score(data["y_test"], predictions["test"])
            
            elif metric == "f1": 
                metrics_out["train"][metric] = sk_metrics.f1_score(data["y_train"], predictions["train"], average = average)
                if valid_exists: 
                    metrics_out["valid"][metric] = sk_metrics.f1_score(data["y_valid"], predictions["valid"], average = average)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.f1_score(data["y_test"], predictions["test"], average = average)
            
            elif metric == "rocauc": 
                metrics_out["train"][metric] = sk_metrics.roc_auc_score(data["y_train"], predictions["train_proba"], average = average, multi_class = "ovr")
                if valid_exists: 
                    metrics_out["valid"][metric] = sk_metrics.roc_auc_score(data["y_valid"], predictions["valid_proba"], average = average, multi_class = "ovr")
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.roc_auc_score(data["y_test"], predictions["test_proba"], average = average, multi_class = "ovr")
            
            elif metric == "prauc": 
                if not multi_class: #only works for binary
                    metrics_out["train"][metric] = sk_metrics.average_precision_score(data["y_train"], predictions["train_proba"][:,1])
                    if valid_exists: 
                        metrics_out["valid"][metric] = sk_metrics.average_precision_score(data["y_valid"], predictions["valid_proba"][:,1])
                    if test_exists:
                        metrics_out["test"][metric] = sk_metrics.average_precision_score(data["y_test"], predictions["test_proba"][:,1])
            
            elif metric == "precision": 
                metrics_out["train"][metric] = sk_metrics.precision_score(data["y_train"], predictions["train"], average = average)
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.precision_score(data["y_valid"], predictions["valid"], average = average)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.precision_score(data["y_test"], predictions["test"], average = average)
           
            elif metric == "recall": 
                metrics_out["train"][metric] = sk_metrics.recall_score(data["y_train"], predictions["train"], average = average)
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.recall_score(data["y_valid"], predictions["valid"], average = average)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.recall_score(data["y_test"], predictions["test"], average = average)
            
            elif metric == "mse": 
                metrics_out["train"][metric] = sk_metrics.mean_squared_error(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.mean_squared_error(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.mean_squared_error(data["y_test"], predictions["test"])
            
            elif metric == "rmse": 
                metrics_out["train"][metric] = sk_metrics.mean_squared_error(data["y_train"], predictions["train"], squared=False)
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.mean_squared_error(data["y_valid"], predictions["valid"], squared=False)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.mean_squared_error(data["y_test"], predictions["test"], squared=False)
            
            elif metric == "mae": 
                metrics_out["train"][metric] = sk_metrics.mean_absolute_error(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.mean_absolute_error(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.mean_absolute_error(data["y_test"], predictions["test"]) 
                
            elif metric == "mape": 
                metrics_out["train"][metric] = sk_metrics.mean_absolute_percentage_error(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.mean_absolute_percentage_error(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.mean_absolute_percentage_error(data["y_test"], predictions["test"])

            elif metric == "mdae": 
                metrics_out["train"][metric] = sk_metrics.median_absolute_error(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.median_absolute_error(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.median_absolute_error(data["y_test"], predictions["test"])

            elif metric == "smape":
                metrics_out["train"][metric] = symmetric_mean_absolute_percentage_error(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = symmetric_mean_absolute_percentage_error(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = symmetric_mean_absolute_percentage_error(data["y_test"], predictions["test"])
                
            elif metric == "r2":  
                metrics_out["train"][metric] = sk_metrics.r2_score(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.r2_score(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.r2_score(data["y_test"], predictions["test"])

            elif metric == "msle":
                metrics_out["train"][metric] = sk_metrics.mean_squared_log_error(data["y_train"], predictions["train"])
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.mean_squared_log_error(data["y_valid"], predictions["valid"])
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.mean_squared_log_error(data["y_test"], predictions["test"])
            
            elif metric == "rmsle":
                #predictions can be negative, which will break this calculation.
                #if you're using rmsle we'll assume you intended non-negative predictions
                for key in set(["train", "valid", "test"]).intersection(predictions.keys()): 
                    predictions[key] = [max(x,0) for x in predictions[key]]
                metrics_out["train"][metric] = sk_metrics.mean_squared_log_error(data["y_train"], predictions["train"], squared=False)
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.mean_squared_log_error(data["y_valid"], predictions["valid"], squared=False)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.mean_squared_log_error(data["y_test"], predictions["test"], squared=False)
  
            

        return metrics_out

    def build_model(self, data, model_version, *args, **kwargs) -> tuple[Any, Any]: 
        """Trains a single model

        Args:
            data (dict): data dictionary of train/test/validation data
            model_version (object): model version

        Returns:
            model: the trained model
            exp: experiment where the model was trained
        """
        #fit model
        model_obj = self.transform_and_fit(data)

        #create experiment and save model 
        experiment = self.metadata_tracker.create_resource(id=None, type="experiment", parent=model_version)
        self.save(experiment)

        #get predictions
        predictions = self.transform_and_predict(data)

        #calculate metrics
        metrics_val = self.calculate_metrics(data, predictions, self._get_config("metrics"))

        #log stuff
        self.metrics_tracker.log_metrics(experiment, metrics_val, self._get_config("perf_metric"))
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_id", data=self.metadata_tracker.get_resource_id(experiment))
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_model_trainer", data = type(self).__name__)

        #save splits
        for k,v in data.items(): 
            vc_info = self.resource_version_control.version_data(model_version, v, key=k)
            self.metadata_tracker.register_vc_resource(model_version, vc_info, key=k, file_type="csv")

        return self, experiment 

    def rebuild_model(self, data, model_version, *args, **kwargs) -> tuple[Any, Any]:
        """Trains model using all available data in the data dictionary

        Args:
            data (dict): dictionary of train/test/validation data
            model_version (object): model version which we want to retrain

        Returns:
            model: newly trained model
            exp: experiment in which the model was trained
        """

        has_test = ("X_test" in data.keys())

        #merge all dfs 
        df_X = pd.concat([data["X_train"], data["X_valid"]])
        df_y = pd.concat([data["y_train"], data["y_valid"]])
        if has_test: 
            df_X = pd.concat([df_X, data["X_test"]])
            df_y = pd.concat([df_y, data["y_test"]])
        train_data = {"X_train" : df_X, "y_train": df_y}

        #get params, class from winning experiment 
        #winning_experiment = self.metadata_tracker.get_winning_experiment(model_version)
        #params = self.metadata_tracker.get_metadata(winning_experiment, "training_params")
        #model_trainer = self.metadata_tracker.get_metadata(winning_experiment, "model_trainer")
        
        #rebuild model on all data 
        model, exp = self.build_model(train_data, model_version)                        
        
        return model, exp
    

def symmetric_mean_absolute_percentage_error(y_true, y_pred):
    """computes symmetric mean absolute percentage error

    Args:
        y_true : actuals
        y_pred : predictions

    Returns:
        float: symmetric mean absoulte percentage error
    """
    epsilon = np.finfo(np.float64).eps
    smape = (2 * np.abs(y_pred - y_true) / np.maximum(np.abs(y_pred) + np.abs(y_true), epsilon))
    return np.average(smape[~np.isnan(smape)])
