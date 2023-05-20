from lolpop.component.base_component import BaseComponent
from sklearn import metrics as sk_metrics
import pandas as pd 

class BaseModelTrainer(BaseComponent): 

    model = None 
    mlflow_module = "you_need_to_implement_this_for_mlflow_use"
    
    #predictions = {}
    def __init__(self, params=None, *args, **kwargs): 
        #set normal config
        super().__init__(params=params, *args, **kwargs)
        if not params: #if params aren't passed in, try to retrieve from config
            params = self._get_config("training_params", {})
        self.params = params

    def fit(self, data, *args, **kwargs): 
        pass 

    def predict(self, data, *args, **kwargs): 
        pass
    
    def save(self, experiment, *args, **kwargs): 
        algo = type(self).__name__
        vc_info = self.resource_version_control.version_model(experiment, self.model, algo=algo)
        experiment_metadata = {
            "training_params" : self.params,
            "model_trainer" : algo
        }
        self.metadata_tracker.register_vc_resource(experiment, vc_info, additional_metadata = experiment_metadata)


    def _predict_df(self, df):
        pass 

    def _predict_proba_df(self, df): 
        pass 

    def _get_model(self):
        return self.model 
    
    #used to set model object. 
    def _set_model(self, model): 
        self.model = model 
    #def _get_predictions(self): 
    #    return self.predictions

    def calculate_metrics(self, data, predictions, metrics, **kwargs): 
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
            if metric == "f1": 
                metrics_out["train"][metric] = sk_metrics.f1_score(data["y_train"], predictions["train"], average = average)
                if valid_exists: 
                    metrics_out["valid"][metric] = sk_metrics.f1_score(data["y_valid"], predictions["valid"], average = average)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.f1_score(data["y_test"], predictions["test"], average = average)
            if metric == "rocauc": 
                metrics_out["train"][metric] = sk_metrics.roc_auc_score(data["y_train"], predictions["train_proba"], average = average, multi_class = "ovr")
                if valid_exists: 
                    metrics_out["valid"][metric] = sk_metrics.roc_auc_score(data["y_valid"], predictions["valid_proba"], average = average, multi_class = "ovr")
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.roc_auc_score(data["y_test"], predictions["test_proba"], average = average, multi_class = "ovr")
            if metric == "prauc": 
                if not multi_class: #only works for binary
                    metrics_out["train"][metric] = sk_metrics.average_precision_score(data["y_train"], predictions["train_proba"][:,1])
                    if valid_exists: 
                        metrics_out["valid"][metric] = sk_metrics.average_precision_score(data["y_valid"], predictions["valid_proba"][:,1])
                    if test_exists:
                        metrics_out["test"][metric] = sk_metrics.average_precision_score(data["y_test"], predictions["test_proba"][:,1])
            if metric == "precision": 
                metrics_out["train"][metric] = sk_metrics.precision_score(data["y_train"], predictions["train"], average = average)
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.precision_score(data["y_valid"], predictions["valid"], average = average)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.precision_score(data["y_test"], predictions["test"], average = average)
            if metric == "recall": 
                metrics_out["train"][metric] = sk_metrics.recall_score(data["y_train"], predictions["train"], average = average)
                if valid_exists:
                    metrics_out["valid"][metric] = sk_metrics.recall_score(data["y_valid"], predictions["valid"], average = average)
                if test_exists:
                    metrics_out["test"][metric] = sk_metrics.recall_score(data["y_test"], predictions["test"], average = average)

        return metrics_out

    def build_model(self, data, model_version, *args, **kwargs): 
        #fit model
        model_obj = self.fit(data)

        #create experiment and save model 
        experiment = self.metadata_tracker.create_resource(id=None, type="experiment", parent=model_version)
        self.save(experiment)

        #get predictions
        predictions = self.predict(data)

        #calculate metrics
        metrics_val = self.calculate_metrics(data, predictions, self._get_config("metrics"))

        #log stuff
        self.metrics_tracker.log_metrics(experiment, metrics_val, self._get_config("perf_metric"))
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_id", data={"winning_experiment_id" : self.metadata_tracker.get_resource_id(experiment)})
        self.metadata_tracker.log_metadata(model_version, id="winning_experiment_model_trainer", data={"winning_experiment_model_trainer" : type(self).__name__})

        #save splits
        for k,v in data.items(): 
            vc_info = self.resource_version_control.version_data(model_version, v, key=k)
            self.metadata_tracker.register_vc_resource(model_version, vc_info, key=k, file_type="csv")

        return self, experiment 

    def rebuild_model(self, data, model_version):
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