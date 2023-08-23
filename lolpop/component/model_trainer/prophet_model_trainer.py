from lolpop.component.model_trainer.base_model_trainer import BaseModelTrainer
from lolpop.utils import common_utils as utils
from prophet import Prophet
from matplotlib import pyplot as plt 

import pandas as pd 
import numpy as np

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ProphetModelTrainer(BaseModelTrainer):

    mlflow_module = "prophet"

    #should set self.model in init
    def __init__(self, problem_type=None, params={}, *args, **kwargs):
        #set normal config
        super().__init__(problem_type=problem_type, params=params, *args, **kwargs)
        self.model = Prophet(**params)

    def fit(self, data, *args, **kwargs):
        """
        Fits the model to the training data.

        Args:
        data: Dictionary containing the training data with columns 'X_train' and 'y_train'

        Output:
        Returns a trained Prophet Model object.
        """
        self.log("Starting model training with parameters: %s" %
                 str(self.params))

        df = data.get("X_train")
        df["y"] = data.get("y_train")
    
        df_train = self._process_data(df)

        country_holidays = self._get_config("country_holidays")
        if country_holidays:
            self.model.add_country_holidays(country_name=country_holidays)

        #add regressors
        regressors = self._get_config("regressor_cols")
        if regressors is not None: 
            regressor_list = regressors.split(",")
            for regressor in regressor_list:
                self.model.add_regressor(regressor)

        self.model.fit(df_train)

        return self.model

    def predict(self, data, *args, **kwargs):
        """
        Predicts values for train, validation and test data.

        Args:
        data: A dictionary containing training, validation and test data with columns 'X_train', 'y_train', 'X_valid', 'y_valid', 'X_test', 'y_test'

        Output:
        Returns a dictionary containing predictions for train, validation and test sets.
        """
        predictions={}
        target_min = self._get_config("target_min")
        target_max = self._get_config("target_max")


        df_train = self._process_data(data["X_train"])
        predictions["train_confidence"] = self._apply_prediction_bounds(
            self.model.predict(df_train), target_min, target_max)
        predictions["train"] = predictions["train_confidence"]["yhat"]
        

        if data.get("X_valid") is not None:
            df_valid= self._process_data(data["X_valid"])
            predictions["valid_confidence"] = self._apply_prediction_bounds(
                self.model.predict(df_valid), target_min, target_max)
            predictions["valid"] = predictions["valid_confidence"]["yhat"]

        if data.get("X_test") is not None:
            df_test = self._process_data(data["X_test"])
            predictions["test_confidence"] = self._apply_prediction_bounds(
                self.model.predict(df_test), target_min, target_max)
            predictions["test"] = predictions["test_confidence"]["yhat"]

        return predictions

    #prophet doesn't seem to do a good job of respecting defined floor/cap on historic data
    #this can cause errors with metrics when numbers are negative, etc 
    def _apply_prediction_bounds(self, data, target_min=None, target_max=None): 
        """
        Applies min/max target values to the predicted values.

        Args:
        data: dataframe containing the predicted values
        target_min: Minimum permissible value for the predicted values
        target_max: Maximum permissible value for the predicted values

        Output:
        Returns a dataframe containing the predicted values within the range of [target_min, target_max].
        """
        data_out = data.copy()
        if target_min is not None: 
            data_out["yhat"] = data["yhat"].apply(lambda x: target_min if x < target_min else x)
        if target_max is not None: 
            data_out["yhat"] = data["yhat"].apply(lambda x: target_max if x > target_max else x) 
        return data_out 


    #def calculate_metrics(self, data, predictions, metrics, **kwargs):
    #    for key in predictions.keys(): 
    #        predictions[key]=predictions[key]["yhat"].to_numpy()
    #    return super().calculate_metrics(data, predictions, metrics, **kwargs) 

    def predict_df(self, df, *args, **kwargs):
        """
        Predicts values for the given dataframe.

        Args:
        df: Dataframe containing the data to be processed

        Output:
        Returns the predicted values.
        """
        data = self._process_data(df)
        return self.model.predict(data)["yhat"]

    def _process_data(self, data): 
        """
        Processes data as per the requirement of Prophet model.

        Args:
        data: Dataframe containing the dataset to be processed.

        Output:
        Returns the processed dataset.
        """

        #prophet expects labels are in a column 'y' and timestamp is 'ds'
        df_train = data.rename(columns={
            self._get_config("time_index"): "ds",
            self._get_config("model_target"): "y",
        }, errors="ignore")

        #set min/max values
        target_min = self._get_config("target_min", None)
        target_max = self._get_config("target_max", None)
        if target_min: 
            df_train["floor"] = target_min
        if target_max: 
            df_train["cap"] = target_max

        data_out = df_train.sort_values("ds").reset_index(drop=True)

        return data_out
    
    def get_artifacts(self, id, *args, **kwargs): 
        """
        Generates plots for visualizing the forecasted data.

        Args:
        id: Id for the model being used for generating plots.

        Output:
        Returns a dictionary containing paths of saved plots.
        """

        artifacts_out  = {}

        # generate component plot
        historic_predictions = self.model.predict(self.model.history)
        self.model.plot_components(historic_predictions)
        local_dir = self._get_config("local_dir")
        file_path = "%s/%s_%s" % (local_dir, id, "component_plot.png")
        plt.savefig(file_path)
        artifacts_out["component_plot"] = file_path 
     
        #plot forecast
        future = self.model.make_future_dataframe(
            periods=self._get_config("forecast_period"), 
            freq=self._get_config("forecast_frequency"),
            include_history=True
            )
        predictions = self.model.predict(future)
        self.model.plot(predictions)
        file_path = "%s/%s_%s" %(local_dir, id, "forecast_plot.png")
        plt.savefig(file_path)
        artifacts_out["forecast_plot"] = file_path

        return artifacts_out
