from lolpop.component.metrics_tracker.base_metrics_tracker import BaseMetricsTracker
from lolpop.component.metadata_tracker.continual_metadata_tracker import ContinualMetadataTracker
from lolpop.utils import continual_utils as cutils
from lolpop.utils import common_utils as utils

#@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class ContinualMetricsTracker(BaseMetricsTracker): 
    __REQUIRED_CONF__ = {
        "config" : ["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"]
    }
    
    def __init__(self, description=None, run_id=None, components = {}, *args, **kwargs): 
        #set normal config
        super().__init__(components = components, *args, **kwargs)
        
        # if we are using continual for metadata tracking then we won't have to set up connection to continual
        # if not, then we do. If would be weird to have to do this, but just in case. 
        if isinstance(components.get("metadata_tracker"), ContinualMetadataTracker): 
            self.client = self.metadata_tracker.client
            self.run = self.metadata_tracker.run
        else: 
            secrets = utils.load_config(["CONTINUAL_APIKEY", "CONTINUAL_ENDPOINT", "CONTINUAL_PROJECT", "CONTINUAL_ENVIRONMENT"], self.config)
            self.client = cutils.get_client(secrets)
            self.run = cutils.get_run(self.client, description=description, run_id=run_id)

    def create_metric(self, resource, id, display_name, **kwargs):
        metric = resource.metrics.create(id=id, display_name=id)
        self.log("Continual metric created: %s" %(metric.name))
        return metric

    def log_metric(self, resource, id, value, group=None, time=None, **kwargs): 
        #first, check to see if metric exists and if not, just create it 
        metric_name = "%s/metrics/%s" %(resource.name,id)
        try: 
            metric = self.get_metric(resource, metric_name)
        except: 
            metric = None 
        if metric is None: 
            metric = self.create_metric(resource, id, id)

        metric_val = metric.log(value=value, group = group, timestamp=time)
        self.log("Created metric value %s/metrics/%s with value %s" %(resource.name, id, value))
        return metric_val
        
    def get_metric(self, resource, id):
        metric = resource.metrics.get(id=id)
        return metric 

    #if latest, returns latest metric, otherwise returns the entire series
    def get_metric_value(self, resource, id, group=None, latest=True):
        if id == "performance_metric_val" or id == "performance_metric_name":
            metric = getattr(resource, id)
            return metric
        else:
            metric = resource.metrics.get(id=id)

            metric_vals = metric.values
            if group is not None:
                metric_vals = [x.value for x in metric_vals if x.group == group]
            if latest:
                metric_vals = metric_vals[-1].value

            return metric_vals

    def log_metrics(self, resource, metrics, perf_metric):
        is_experiment = resource.name.split("/")[-2] == "experiments"

        if is_experiment: 
            #set performance metric for experiment 
            resource.performance_metric_name = perf_metric

            if len(metrics.get("valid")) > 0: 
                resource.performance_metric_val = metrics["valid"][perf_metric]
            else: 
                resource.performance_metric_val = metrics["train"][perf_metric]
            resource.update(paths=["performance_metric_name", "performance_metric_val"])

        #create metrics object for each metric
        metrics_dicts = cutils.convert_to_metrics_dicts(metrics)
        for key in metrics["train"].keys(): 
            self.create_metric(resource, id=key, display_name=key)

        #log all metrics 
        for metric in metrics_dicts: 
            self.log_metric(resource, **metric)
    
    #copy metrics from one resource to another. 
    #Mainly used to copy winning exp metrics to model version
    def copy_metrics(self, from_resource, to_resource, to_type="model_version"): 
        #iterate through all metrics in from_resource. these will have types Metric
        for old_metric in from_resource.metrics.list_all(): 
            #create new metric for each metric
            new_metric = self.create_metric(to_resource,id=old_metric.id, display_name=old_metric.display_name)
            #iterate through all metric vaules in old_metric. These will have type MetricValue
            for value in old_metric.values(): 
                #log a new value for each MetricValue
                new_metric.log( 
                    value = value.value, 
                    group = value.group, 
                    timestamp = value.timestamp, 
                    step = value.step, 
                    label = value.label,
                )
        if to_type == "model_version": 
            to_resource.update(
                performance_metric_name = from_resource.performance_metric_name,
                performance_metric_val = from_resource.performance_metric_val
                )
        elif to_type =="experiment": 
            to_resource.performance_metric_name = from_resource.performance_metric_name
            to_resource.performance_metric_val = from_resource.performance_metric_val
            to_resource.update(paths=["performance_metric_name", "performance_metric_val"])

    def log_prediction_metrics(self, prediction_job, predictions): 
        df_values = predictions.value_counts()
        class_distribution = {x:y/sum(df_values) for x,y in df_values.to_dict().items()}

        self.metadata_tracker.log_metadata(prediction_job, id="class_distribution", data = class_distribution)
        self.log_metric(prediction_job, "num_predictions", len(predictions))