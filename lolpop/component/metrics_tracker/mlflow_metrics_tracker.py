from lolpop.component.metrics_tracker.base_metrics_tracker import BaseMetricsTracker
from lolpop.utils import common_utils as utils
#import your libraries here
from lolpop.component.metadata_tracker.mlflow_metadata_tracker import MLFlowMetadataTracker
from lolpop.utils import mlflow_utils
import json 
import mlflow

@utils.decorate_all_methods([utils.error_handler, 
                             utils.log_execution(), 
                             mlflow_utils.check_active_mlflow_run(mlflow)])
class MLFlowMetricsTracker(BaseMetricsTracker):
    #Override required or default configurations here for your class
    ##Add required configuration here
    __REQUIRED_CONF__ = {
        "component" : ["metadata_tracker|MLFlowMetadataTracker"],
        #"config": ["mlflow_tracking_uri", "mlflow_experiment_name"]
    }
    ##Add default configuration here
    #__DEFAULT_CONF__ = {
    #    "config": {}
    #}

    def __init__(self, dependent_integrations=None, *args, **kwargs):
        if dependent_integrations is None: 
            dependent_integrations = {}
        #set normal config
        super().__init__(dependent_integrations=dependent_integrations, *args, **kwargs)

        # if we are using mlflow for metadata tracking then we won't have to set up connection to mlflow
        # if not, then we do. If would be weird to have to do this, but just in case.
        if isinstance(dependent_integrations.get("component",{}).get("metadata_tracker"), MLFlowMetadataTracker):
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
            self.url = self.metadata_tracker.url
        else: #we should only use this if we allow metrics tracking w/o metadata tracking
            tracking_uri = self._get_config("mlflow_tracking_uri")
            experiment_name = self._get_config("mlflow_experiment_name")

            self.client, self.run = mlflow_utils.connect(tracking_uri, experiment_name)
            self.url = tracking_uri

            self.log("Using MLFlow in experiment %s with run id: %s" %(experiment_name, self.run.info.run_id), level="INFO")

    def log_metric(self, resource, id, value, *args, **kwargs): 
        """
        Logs a metric with the corresponding resource ID, metric ID, and metric value

        Args:
            resource (object): A resource object
            id (str): A unique identifier for the metric
            value (Any): The value of the metric

        Returns:
            None
        """
        run_id = resource[1].info.run_id
        resource_id = self.metadata_tracker.get_resource_id(resource)
        id = "%s.%s" %(resource_id, id)
        self.client.log_metric(run_id, id, value, **kwargs)
        self.log("Saving metric=%s, value=%s in run %s" % (id, value, run_id))
        
    def get_metric(self, resource, id, *args, **kwargs):
        """
        Retrieves a metric with the corresponding resource ID and metric ID

        Args:
            resource: A resource object
            id: The metric ID

        Returns:
            metric: The value of the metric or None if the metric is not found
        """
        run = mlflow_utils.get_run(self.client, resource[1].info.run_id)
        resource_id = self.metadata_tracker.get_resource_id(resource)
        id = "%s.%s" % (resource_id, id)
        metric =  run.data.metrics.get(id)
        return metric 

    def log_metrics(self, resource, metrics, perf_metric, *args, **kwargs):
        """
        Logs multiple metrics with the corresponding resource ID and specified performance metric

        Args:
            resource: A resource object
            metrics: A dictionary containing the metrics
            perf_metric: A performance metric

        Returns:
            None
        """
        for split in metrics.keys(): 
            for metric, val in metrics[split].items(): 
                key = "%s_%s" %(split, metric)
                self.log_metric(resource, key, val)

        self.metadata_tracker.log_metadata(resource, "performance_metric", perf_metric)
        if len(metrics.get("valid")) > 0:
            self.metadata_tracker.log_metadata(resource, "performance_metric_value", metrics["valid"][perf_metric])
        else:
            self.metadata_tracker.log_metadata(resource, "performance_metric_value", metrics["train"][perf_metric])
    
    #copy metrics from one resource to another. 
    #Mainly used to copy winning exp metrics to model version
    def copy_metrics(self, from_resource, to_resource, *args, **kwargs): 
        """
        Copies metrics from one resource to another

        Args:
            from_resource: The resource to copy metrics from
            to_resource: The resource to copy metrics to
        Returns:
            None
        """
        from_run = mlflow_utils.get_run(self.client, from_resource[1].info.run_id)

        for k,v in from_run.data.metrics.items():
            key = k.split(".")[-1] 
            self.log_metric(to_resource, key, v)

        self.metadata_tracker.log_metadata(
            to_resource,
            "performance_metric", 
            self.metadata_tracker.get_metadata(from_resource, "performance_metric"))
        self.metadata_tracker.log_metadata(
            to_resource,
            "performance_metric_value",
            self.metadata_tracker.get_metadata(from_resource, "performance_metric_value"))
        self.metadata_tracker.log_metadata(
            to_resource, 
            "training_params", 
            utils.parse_dict_string(self.metadata_tracker.get_metadata(from_resource, "training_params"))
        )

    def log_prediction_metrics(self, prediction_job, predictions, *args, **kwargs):
        """
        Logs prediction metrics with the corresponding prediction job ID and list of predictions

        Args:
            prediction_job: A prediction job
            predictions: A list of predictions

        Returns:
            None
        """
        prediction_id = self.metadata_tracker.get_resource_id(prediction_job)
        if self.problem_type == "classification":  
            df_values = predictions.value_counts()
            class_distribution = {x:y/sum(df_values) for x,y in df_values.to_dict().items()}
            self.metadata_tracker.log_metadata(prediction_job, id="class_distribution", data = class_distribution)

        self.log_metric(
            prediction_job, "num_predictions", len(predictions))
