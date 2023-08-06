from lolpop.component.base_component import BaseComponent
from lolpop.utils import common_utils as utils
import numpy as np 
from typing import Any 

class BaseModelChecker(BaseComponent): 

    __REQUIRED_CONF__ = {"components": ["metrics_tracker"],
                         "config": ["baseline_method", "baseline_value", "perf_metric"]}

    def check_model(self, data, model, *args, **kwargs) -> tuple[Any, str, str]:
        pass 

    def calculate_model_drift(self, data, model, deployed_model, *args, **kwargs) -> tuple[Any, str]:
        pass

    def get_baseline_comparison(self, data, model, model_version, *args, **kwargs) -> tuple[bool, float]:
        """
        Compare the model performance against a baseline.

        Args:
            data: The data for model evaluation.
            model: The trained model object.
            model_version: The version of the model.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The metric difference between the model and the baseline.

        """

        #TODO: we are already getting predictions elsewhere. 
        #We should just save them and pass in instead of calculating again
        baseline_method = self._get_config("baseline_method")
        baseline_value = self._get_config("baseline_value")
        test_predictions = model.predict(data)
        baseline_predictions = self._get_baseline_predictions(data, baseline_method, baseline_value)

        #TODO: model metrics are being recalculated here, should save and load
        perf_metric = self._get_config("perf_metric")
        model_metrics = model.calculate_metrics(data, test_predictions, [perf_metric])
        baseline_metrics = model.calculate_metrics(data, baseline_predictions, [perf_metric])
        for split in baseline_metrics.keys(): 
            self.metrics_tracker.log_metric(model_version, "baseline_%s_%s" %(split, perf_metric), baseline_metrics[split][perf_metric])
        is_baseline_better, metric_diff = self._get_metric_comparison(model_metrics, baseline_metrics, perf_metric)

        self.metrics_tracker.log_metric(model_version, "model_test_performance_over_baseline", metric_diff)

        if is_baseline_better: 
            self.notify("Model performed worse than baseline by %s%%" %metric_diff, level="WARN")

        return is_baseline_better, metric_diff 

    def compare_models(self, data, model, prev_model, model_version, prev_model_version=None, *args, **kwargs) -> bool: 
        """
        Compare the performance of the current model against the previous model.

        Args:
            data: The data for model evaluation.
            model: The current trained model object.
            prev_model: The previous trained model object.
            model_version: The version of the current model.
            prev_model_version: The version of the previous model (default None).
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if the current model is better than the previous model, False otherwise.

        """
        #this should only happen during the first training of a model
        if prev_model_version == model_version:
            is_new_model_better = True 
        else: 
            perf_metric = self._get_config("perf_metric")
            is_new_model_better, metric_diff = self._compare_model_performance(model, prev_model, data, perf_metric, model_version)

        return is_new_model_better

    #default implementation of baseline predictions
    def _get_baseline_predictions(self, data, baseline_method, baseline_value, *args, **kwargs) -> dict[str,Any]: 
        """
        Get baseline predictions based on the baseline method and value.

        Args:
            data: The data for baseline comparison.
            baseline_method: The method for baseline comparison.
            baseline_value: The value used in baseline comparison.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the baseline predictions for different data splits.

        """
        has_test = "X_test" in data.keys()
        has_valid = "X_valid" in data.keys()
        baseline_predictions = {}

        #column = user defined column should be used for baseline comparison
        if baseline_method == "column": 
            baseline_predictions["train"] = data["X_train"][baseline_value]
            baseline_predictions["valid"] = data["X_valid"][baseline_value]
            if has_test: 
                baseline_predictions["test"] = data["X_test"][baseline_value]

        elif baseline_method == "value":
            if self.problem_type == "classification":    
                labels = data["y_train"]
                #this is kind of hacky but ... shrug
                labels.index=labels.values
                label_counts = labels.groupby(level=0).count()

                #classification
                if baseline_value == "class_avg": 
                    weights = [x/len(labels) for x in label_counts]
                    baseline_predictions["train"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_train"]))
                    baseline_predictions["valid"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_valid"]))
                    if has_test: 
                        baseline_predictions["test"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_test"]))

                #classification
                elif baseline_value == "class_most_frequent": 
                    most_frequent_class = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[0][0] #get most frequent class 
                    baseline_predictions["train"] = [most_frequent_class] * len(data["X_train"])
                    baseline_predictions["valid"] = [most_frequent_class] * len(data["X_valid"])
                    if has_test: 
                        baseline_predictions["test"] = [most_frequent_class] * len(data["X_test"])
            
            elif self.problem_type == "regression":
                labels = data["y_train"]

                if baseline_value == "avg": 
                    mean = labels.mean()
                    baseline_predictions["train"] = [mean] * len(data["X_train"])
                    baseline_predictions["valid"] = [mean] * len(data["X_valid"])
                    if has_test: 
                        baseline_predictions["test"] = [mean] * len(data["X_test"])

                if baseline_value == "mode": 
                    mode = labels.mode()[0]
                    baseline_predictions["train"] = [mode] * len(data["X_train"])
                    baseline_predictions["valid"] = [mode] * len(data["X_valid"])
                    if has_test: 
                        baseline_predictions["test"] = [mode] * len(data["X_test"])

                if baseline_value == "max": 
                    max = labels.max()
                    baseline_predictions["train"] = [max] * len(data["X_train"])
                    baseline_predictions["valid"] = [max] * len(data["X_valid"])
                    if has_test: 
                        baseline_predictions["test"] = [max] * len(data["X_test"])

                if baseline_value == "min": 
                    min = labels.min()
                    baseline_predictions["train"] = [min] * len(data["X_train"])
                    baseline_predictions["valid"] = [min] * len(data["X_valid"])
                    if has_test: 
                        baseline_predictions["test"] = [min] * len(data["X_test"])
                        
                if baseline_value == "median": 
                    median = labels.median()
                    baseline_predictions["train"] = [median] * len(data["X_train"])
                    baseline_predictions["valid"] = [median] * len(data["X_valid"])
                    if has_test: 
                        baseline_predictions["test"] = [median] * len(data["X_test"])

            elif self.problem_type == "timeseries":
                #time series . should be in the form 'last_value_N'
                if baseline_value.startswith("last_value"):
                    shift_value = int(baseline_value.split("_")[-1]) 
                    baseline_predictions["train"] = data["y_train"].shift(shift_value)
                    if has_valid: 
                        baseline_predictions["valid"] = data["y_valid"].shift(shift_value)
                    if has_test: 
                        baseline_predictions["test"] = data["y_test"].shift(shift_value)
                        
                elif baseline_value.startswith("lag_mean"):
                    window_size = int(baseline_value.split("_")[-1])
                    baseline_predictions["train"] = data["y_train"].shift(1).rolling(window_size, min_periods=1).mean()
                    if has_valid: 
                        baseline_predictions["valid"] = data["y_valid"].shift(1).rolling(window_size, min_periods=1).mean()
                    if has_test: 
                        baseline_predictions["test"] = data["y_test"].shift(1).rolling(window_size, min_periods=1).mean()

                elif baseline_value.startswith("lag_max"):
                    window_size = int(baseline_value.split("_")[-1])
                    baseline_predictions["train"] = data["y_train"].shift(
                        1).rolling(window_size, min_periods=1).max()
                    if has_valid:
                        baseline_predictions["valid"] = data["y_valid"].shift(
                            1).rolling(window_size, min_periods=1).max()
                    if has_test:
                        baseline_predictions["test"] = data["y_test"].shift(
                            1).rolling(window_size, min_periods=1).max()
                        
                elif baseline_value.startswith("lag_min"):
                    window_size = int(baseline_value.split("_")[-1])
                    baseline_predictions["train"] = data["y_train"].shift(
                        1).rolling(window_size, min_periods=1).min()
                    if has_valid:
                        baseline_predictions["valid"] = data["y_valid"].shift(
                            1).rolling(window_size, min_periods=1).min()
                    if has_test:
                        baseline_predictions["test"] = data["y_test"].shift(
                            1).rolling(window_size, min_periods=1).min()
                        
                elif baseline_value.startswith("lag_median"):
                    window_size = int(baseline_value.split("_")[-1])
                    baseline_predictions["train"] = data["y_train"].shift(
                        1).rolling(window_size, min_periods=1).median()
                    if has_valid:
                        baseline_predictions["valid"] = data["y_valid"].shift(
                            1).rolling(window_size, min_periods=1).median()
                    if has_test:
                        baseline_predictions["test"] = data["y_test"].shift(
                            1).rolling(window_size, min_periods=1).median()
                        
                #first value will be NaN, so set it to the second just to prevent errors. 
                for key in baseline_predictions.keys(): 
                    baseline_predictions[key].iloc[0]=baseline_predictions[key].iloc[1]

        else: #consider other ways to do baseline comparison
            pass

        return baseline_predictions 

    def _get_metric_comparison(self, champion_metric, challenger_metric, perf_metric, *args, **kwargs) -> tuple[bool, float]: 
        """Compares two metric values and determines which is better. 

        Args:
            champion_metric (dict): champion metric
            challenger_metric (dict): challenger metric
            perf_metric (str): The performance metric to use to determine which metric is best

        Returns:
            bool: is the challenger metric better? True or False 
            float: difference between champion and challenger metric
        """
        old_metric = champion_metric.get("test").get(perf_metric)
        new_metric = challenger_metric.get("test").get(perf_metric)
        lower_is_better = not utils.get_metric_direction(perf_metric)

        if lower_is_better: #True = perf_metric is better if lower
            is_challenger_better = (new_metric < old_metric) 
            metric_diff = (new_metric - old_metric) / max(old_metric, 0.00001) * 100
        else: #wants higher perf metric
            is_challenger_better = (new_metric > old_metric)
            metric_diff = (old_metric - new_metric) / max(old_metric, 0.00001) * 100 

        return is_challenger_better, metric_diff

    def _compare_model_performance(self, model, deployed_model, data, perf_metric, current_model_version, *args, **kwargs) -> tuple[bool, float]: 
        """Commpares model performance to deployed model against a static data set. 

        Args:
            model (object): current model
            deployed_model (object): deployed model
            data (dictionary): dicitonary of training/test data
            perf_metric (_type_): performance metric to use to determine which model is better
            current_model_version (_type_): current model verison to log metrics into

        Returns:
            bool: Is the new model better? True or False
            float: difference between metric values
        """
        current_predictions = model.predict(data)
        deployed_predictions = deployed_model.predict(data)

        current_metrics = model.calculate_metrics(data, current_predictions, [perf_metric])
        deployed_metrics = deployed_model.calculate_metrics(data, deployed_predictions, [perf_metric])

        is_new_model_better, metric_diff = self._get_metric_comparison(deployed_metrics, current_metrics, perf_metric)

        self.metrics_tracker.log_metric(current_model_version, "deployed_model_perf_metric_diff", metric_diff)

        return is_new_model_better, metric_diff