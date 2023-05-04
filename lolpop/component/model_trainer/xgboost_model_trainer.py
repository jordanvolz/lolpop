from lolpop.component.model_trainer.base_model_trainer import BaseModelTrainer
from lolpop.utils import common_utils as utils
from xgboost import XGBClassifier, XGBRegressor 

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class XGBoostModelTrainer(BaseModelTrainer): 

    mlflow_module = "xgboost"

    #should set self.model in init
    def __init__(self, problem_type=None, params={}, *args, **kwargs): 
        #set normal config
        super().__init__(problem_type = problem_type, params=params, *args, **kwargs)
 
        #set up model based on problem_type
        if self.problem_type == "classification": 
            self.model = XGBClassifier(**params)
        elif self.problem_type == "regression": 
            self.model == XGBRegressor(**params)
        else: 
            msg = "Unsupported problem type (%s) in trainer %s" %(problem_type, self.name)
            self.notify(msg)
            raise Exception(msg)


    def fit(self, data, *args, **kwargs): 
        self.log("Starting model training with parameters: %s" %str(self.params))
        self.model.fit(data["X_train"], data["y_train"])
        self.log("Finished model training.")
        return self.model  

    def predict(self, data, *args, **kwargs):
        predictions = {}

        predictions["train"] = self.model.predict(data["X_train"])
        if self.problem_type == "classification": 
            predictions["train_proba"] = self.model.predict_proba(data["X_train"])

        if data.get("X_valid") is not None: 
            predictions["valid"] = self.model.predict(data["X_valid"])
            if self.problem_type == "classification": 
                predictions["valid_proba"] = self.model.predict_proba(data["X_valid"])

        if data.get("X_test") is not None: 
            predictions["test"] = self.model.predict(data["X_test"])
            if self.problem_type == "classification": 
                predictions["test_proba"] = self.model.predict_proba(data["X_test"])

        #self.predictions = predictions

        return predictions 

    #def save(self, experiment, *args, **kwargs): 
    #    pass

    def _predict_df(self,df): 
        return self.model.predict(df)

    def _predict_proba_df(self,df, to_list=False): 
        predictions = self.model.predict_proba(df)
        if to_list: 
            predictions = predictions.tolist()
        return predictions