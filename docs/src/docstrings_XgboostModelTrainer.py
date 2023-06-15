```
class XGBoostModelTrainer(BaseModelTrainer):
    """A class for training and using XGBoost models for classification or regression.

    Args:
        problem_type (str): Problem type of classification or regression.
        params (dict): Dictionary of XGBoost model parameters.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        mlflow_module (str): Name of the mlflow module.
        model: XGBoost model object.

    """
    mlflow_module = "xgboost"

    def __init__(self, problem_type=None, params={}, *args, **kwargs):
        """Initializes XGBoostModelTrainer instance.

        Args:
            problem_type (str): Problem type of classification or regression.
            params (dict): Dictionary of XGBoost model parameters.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Raises:
            Exception: If problem_type is unsupported.

        """
        super().__init__(problem_type = problem_type, params=params, *args, **kwargs)
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

    def predict_df(self, df):
        """Performs prediction using the XGBoost model on a pandas DataFrame.

        Args:
            df (pandas DataFrame): Dataframe containing input features.

        Returns:
            numpy array: Predicted output.

        """
        return self.model.predict(df)

    def predict_proba_df(self, df, to_list=False):
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
```