from lolpop.component.base_component import BaseComponent
from lolpop.utils import common_utils as utils
import numpy as np 

class BaseModelChecker(BaseComponent): 

    def check_model(self, data, model, **kwargs): 
        pass 


    def get_baseline_comparison(self, data, model, model_version):

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

        return metric_diff 

    def compare_models(self, data, model, prev_model, model_version, prev_model_version=None): 
        #this should only happen during the first training of a model
        if prev_model_version == model_version:
            is_new_model_better = True 
        else: 
            perf_metric = self._get_config("perf_metric")
            is_new_model_better, metric_diff = self._compare_model_performance(model, prev_model, data, perf_metric, model_version)

        return is_new_model_better

    #default implementation of baseline predictions
    def _get_baseline_predictions(self, data, baseline_method, baseline_value): 
        
        has_test = "X_test" in data.keys()
        baseline_predictions = {}

        #column = user defined column should be used for baseline comparison
        if baseline_method == "column": 
            baseline_predictions["train"] = data["X_train"][baseline_value]
            baseline_predictions["valid"] = data["X_valid"][baseline_value]
            if has_test: 
                baseline_predictions["test"] = data["X_test"][baseline_value]

        elif baseline_method == "value":    
            labels = data["y_train"]
            #this is kind of hacky but ... shrug
            labels.index=labels.values
            label_counts = labels.groupby(level=0).count()

            if baseline_value == "class_avg": 
                weights = [x/len(labels) for x in label_counts]
                baseline_predictions["train"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_train"]))
                baseline_predictions["valid"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_valid"]))
                if has_test: 
                    baseline_predictions["test"] = np.random.choice(label_counts.index, p=weights, size=len(data["X_test"]))

            elif baseline_value == "class_most_frequent": 
                most_frequent_class = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[0][0] #get most frequent class 
                baseline_predictions["train"] = [most_frequent_class] * len(data["X_train"])
                baseline_predictions["valid"] = [most_frequent_class] * len(data["X_valid"])
                if has_test: 
                    baseline_predictions["test"] = [most_frequent_class] * len(data["X_test"])

        else: #consider other ways to do baseline comparison
            pass

        return baseline_predictions 

    def _get_metric_comparison(self, champion_metric, challenger_metric, perf_metric): 
        old_metric = champion_metric.get("test").get(perf_metric)
        new_metric = challenger_metric.get("test").get(perf_metric)
        lower_is_better = utils.get_metric_direction(perf_metric)

        if lower_is_better: #True = perf_metric is better if lower
            is_challenger_better = (new_metric < old_metric) 
            metric_diff = (new_metric - old_metric) / max(old_metric, 0.00001) * 100
        else: #wants higher perf metric
            is_challenger_better = (new_metric > old_metric)
            metric_diff = (old_metric - new_metric) / max(old_metric, 0.00001) * 100 

        return is_challenger_better, metric_diff

    def _compare_model_performance(self, model, deployed_model, data, perf_metric, current_model_version): 
        current_predictions = model.predict(data)
        deployed_predictions = deployed_model.predict(data)

        current_metrics = model.calculate_metrics(data, current_predictions, [perf_metric])
        deployed_metrics = deployed_model.calculate_metrics(data, deployed_predictions, [perf_metric])

        is_new_model_better, metric_diff = self._get_metric_comparison(deployed_metrics, current_metrics, perf_metric)

        self.metrics_tracker.log_metric(current_model_version, "deployed_model_perf_metric_diff", metric_diff)

        return is_new_model_better, metric_diff

    def calculate_model_drift(self, data, model, deployed_model, **kwargs):
        pass