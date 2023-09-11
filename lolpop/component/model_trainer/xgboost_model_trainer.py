from lolpop.component.model_trainer.base_model_trainer import BaseModelTrainer
from lolpop.utils import common_utils as utils
from xgboost import XGBClassifier, XGBRegressor 

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class XGBoostModelTrainer(BaseModelTrainer): 

    mlflow_module = "xgboost"

    def __init__(self, problem_type=None, params={}, *args, **kwargs): 
        #set normal config
        super().__init__(problem_type = problem_type, params=params, *args, **kwargs)
 
        #set up model based on problem_type
        if self.problem_type == "classification": 
            self.model = XGBClassifier(**params)
        elif self.problem_type == "regression": 
            self.model = XGBRegressor(**params)
        else: 
            msg = "Unsupported problem type (%s) in trainer %s" %(problem_type, self.name)
            self.notify(msg)
            raise Exception(msg)


    def fit(self, data, *args, **kwargs): 
        """Fits XGBoost model on given data.

        Args:
            data (dict): Dictionary containing input features X_train, y_train, X_valid, and X_test.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            XGBoost model object.

        """
        self.log("Starting model training with parameters: %s" %str(self.params))
        self.model.fit(data["X_train"], data["y_train"])
        self.log("Finished model training.")
        return self.model  

    def predict(self, data, *args, **kwargs):
        """Performs prediction using the XGBoost model.

        Args:
            data (dict): Dictionary containing input features X_train, y_train, X_valid, and X_test.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: Dictionary containing train, valid, and test predictions and probablities if applicable.

        """
        predictions = {}
        
        data_train = self._order_features(data["X_train"])
        predictions["train"] = self.model.predict(data_train)
        if self.problem_type == "classification": 
            predictions["train_proba"] = self.model.predict_proba(data_train)

        if data.get("X_valid") is not None: 
            data_valid = self._order_features(data["X_valid"])
            predictions["valid"] = self.model.predict(data_valid)
            if self.problem_type == "classification": 
                predictions["valid_proba"] = self.model.predict_proba(data_valid)

        if data.get("X_test") is not None: 
            data_test = self._order_features(data["X_test"])
            predictions["test"] = self.model.predict(data_test)
            if self.problem_type == "classification": 
                predictions["test_proba"] = self.model.predict_proba(data_test)

        #self.predictions = predictions

        return predictions 


    def predict_df(self, df, *args, **kwargs): 
        """Performs prediction using the XGBoost model on a pandas DataFrame.

        Args:
            df (pandas DataFrame): Dataframe containing input features.

        Returns:
            numpy array: Predicted output.

        """
        return self.model.predict(self._order_features(df))

    def predict_proba_df(self,df, to_list=False, *args, **kwargs): 
        """Performs prediction probabilities estimation of the model on a pandas DataFrame.

        Args:
            df (pandas DataFrame): Dataframe containing input features.
            to_list (bool): Whether to convert the probabilities into a list.

        Returns:
            numpy array or list: Predicted probabilities.

        """
        predictions = self.model.predict_proba(df)
        if to_list: 
            predictions = predictions.tolist()
        return predictions
    
    def _get_feature_names(self, *args, **kwargs):
        """Returns a list of feature names. Mainly used to determine the correct order 
        for passing in feature columns when making predictions
        """ 
        return self.model.feature_names_in_
    
    def _order_features(self, data, *args, **kwargs):
        """Orders the features in the provided data

        Args:
            data (object): Data object containing features. 

        Returns:
            data_out: Data object with the correct order of features
        """
        data_out = data
        feature_names = self._get_feature_names()
        if feature_names is not None:
            data_out = data[feature_names]
        return data_out
