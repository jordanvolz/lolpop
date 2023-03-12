from runner.abstract_runner import AbstractRunner
from utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ClassificationRunner(AbstractRunner):

    __REQUIRED_CONF__ = {
        "pipelines": ["process", "train", "deploy", "predict"],
        "components": ["metadata_tracker", "metrics_tracker", "resource_version_control"],
        "config": ["table_train", "table_eval", "table_prediction", "model_target", "drop_columns"]
    }

    def __init__(self, conf):
        super().__init__(conf, problem_type="classification")

    def process_data(self, source_data = "train"):
        #run data transformations and encodings
        source_table_name = self.config.get("table_%s" % source_data)
        data = self.process.transform_data(source_table_name)  # maybe better called get_training_data?

        #track & version data
        dataset_version = self.process.track_data(data, source_table_name)

        #profile data
        self.process.profile_data(data, dataset_version)

        #run data checks
        self.process.check_data(data, dataset_version)

        #run data comparison/drift
        self.process.compare_data(data, dataset_version)

        #return data
        return data, dataset_version

    def train_model(self, data, dataset_version=None):

        if data is None:
            if dataset_version is not None:
                data = self.resource_version_control.get_data(
                    dataset_version, self.metadata_tracker.get_vc_info(dataset_version))
            else:
                self.notify(
                    "No data provided. Can't train a model", level="ERROR")
                raise Exception("No data provided. Can't train a model.")

        #split data
        data_dict = self.train.split_data(data)

        #train a model
        model, model_version = self.train.train_model(data_dict)

        #analyze the model
        self.train.analyze_model(data_dict, model, model_version)

        #run model checks
        self.train.check_model(data_dict, model, model_version)

        #run bias checks
        self.train.check_model_bias(data_dict, model, model_version)

        #build lineage
        self.metadata_tracker.build_model_lineage(
            model_version, self.process.datasets_used)

        #run comparison to previous model verison
        is_new_model_better = self.train.compare_models(
            data_dict, model, model_version)

        #if new model is better, retrain on all data if specified
        if is_new_model_better:
            if self.train._get_config("retrain_all"):
                model, experiment = self.train.retrain_model_on_all_data(
                    data_dict, model_version, ref_model=model)

        return model_version, model, is_new_model_better

    def deploy_model(self, model_version):
        #promote model
        promotion = self.deploy.promote_model(model_version)

        #check if model is approved
        is_approved = self.deploy.check_approval(promotion)

        #if approved, deploy model
        if is_approved:
            deployment = self.deploy.deploy_model(promotion, model_version)

        return deployment

    def predict_data(self, model_version, model, data, dataset_version):
        if model is None: 
            if model_version is not None: 
                experiment = self.metadata_tracker.get_winning_experiment(model_version)
                model_obj = self.resource_version_control.get_model(experiment, key="model_artifact")
                model = self.train.load_model(model_obj, model_version, model)
        
        #compare evaluation data to training data
        self.predict.compare_data(model_version, dataset_version, data)

        #get predictions
        data, prediction_job = self.predict.get_predictions(model, model_version, data)

        #version data
        self.predict.track_predictions(prediction_job, data)

        #calculate drift
        self.predict.analyze_prediction_drift(dataset_version, prediction_job, data)

        #run prediction checks
        self.predict.check_predictions(data.drop(["explanations", "predictions_proba"],axis=1, errors="ignore"), prediction_job)

        #run save predictions
        self.predict.save_predictions(data, self._get_config("table_prediction"))

        return data, prediction_job

    def evaluate_ground_truth(self, prediction_job=None): 
        #if prediction job isn't known, get the most recent job
        if prediction_job == None: 
            model = self.metadata_tracker.get_resource(self.config.get("model_name"), type="model")
            prediction_job = self.metadata_tracker.get_latest_model_resource(model, type="prediction_job")
        
        #get prediciton data 
        vc_info = self.metadata_tracker.get_vc_info(prediction_job)
        prediction_data = self.resource_version_control.get_data(prediction_job, vc_info, key = "data_csv") 

        #get *current* training data
        train_data = self.process.transform_data(self.config.get("table_train"))

        #train data might have a lot more data than when we predicted, so we need to 
        #filter out extra data and then match indices 
        index = self._get_config("model_index")
        train_data_filtered = train_data[train_data[index].isin(prediction_data[index])]
        train_data_sorted = train_data_filtered.sort_values(by=index).reset_index(drop=True)
        prediction_data_sorted = prediction_data.sort_values(by=index).reset_index(drop=True)
        ground_truth = {"y_train": train_data_sorted[self.config.get("model_target")]}
        predictions = {"train": prediction_data_sorted["predictions"]}

        #get model object and calculate metrics
        model_version = self.metadata_tracker.get_prediction_job_model_version(prediction_job)
        experiment = self.metadata_tracker.get_winning_experiment(model_version)
        model_obj = self.resource_version_control.get_model(experiment, key="model_artifact")
        model = self.train.load_model(model_obj, model_version, None)
        metrics_val = model.calculate_metrics(ground_truth, predictions, self.train._get_config("metrics"))

        #log stuff
        self.metrics_tracker.log_metrics(prediction_job, metrics_val, self.train._get_config("perf_metric"))
        self.metrics_tracker.log_metric(
            prediction_job, "num_ground_truth_observations", train_data_sorted.shape[0])

    def stop(self):
        self.metadata_tracker.stop()
        pass

    def build_all(self):
        data, dataset_version = self.process_data()
        model_version, model, is_new_model_better = self.train_model(data, dataset_version)
        if is_new_model_better: 
            deployment = self.deploy_model(model_version)
        eval_data, eval_dataset_version = self.process_data(source_data="eval")
        data, prediction_job = self.predict_data(model_version,model, eval_data, eval_dataset_version)
        self.evaluate_ground_truth(prediction_job)
        
    #helper function for lookup up config key 
    def _get_config(self, key, default_value=None):
        key = key.lower()
        value = utils.lower_conf(self.config).get(key, None)
        return value
