from lolpop.runner.base_runner import BaseRunner
from lolpop.utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ClassificationRunner(BaseRunner):

    __REQUIRED_CONF__ = {
        "pipelines": ["process", "train", "deploy", "predict"],
        "components": ["metadata_tracker", "metrics_tracker", "resource_version_control"],
        "config": ["train_data", "eval_data", "prediction_data", "model_target", "drop_columns"]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(problem_type="classification", *args, **kwargs)

    def process_data(self, source_data = "train"):
        #run data transformations and encodings
        source_data_name = self._get_config("%s_data" % source_data)
        data = self.process.transform_data(source_data_name)  # maybe better called get_training_data?

        #track & version data
        dataset_version = self.process.track_data(data, source_data_name)

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

    def deploy_model(self, model_version, model):
        #promote model
        promotion = self.deploy.promote_model(model_version, model)

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
                model_obj = self.resource_version_control.get_model(experiment)
                model = self.metadata_tracker.load_model(model_obj, model_version, model)
        
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
        self.predict.save_predictions(data, self._get_config("prediction_data"))

        return data, prediction_job

    def evaluate_ground_truth(self, prediction_job=None): 
        #if prediction job isn't known, get the most recent job
        if prediction_job == None: 
            model = self.metadata_tracker.get_resource(self._get_config("model_name"), type="model")
            prediction_job = self.metadata_tracker.get_latest_model_resource(model, type="prediction_job")
        
        #get prediciton data 
        vc_info = self.metadata_tracker.get_vc_info(prediction_job)
        prediction_data = self.resource_version_control.get_data(prediction_job, vc_info) 
        
        #get *current* training data
        train_data = self.process.transform_data(self._get_config("train_data"))
        
        #let's find common index values that exist in both the training dataset and the prediction set
        index = self._get_config("model_index")
        common_indices = train_data.merge(prediction_data, on=index, how="inner")[index]

        #if there are any in common, then we can check the ground truth 
        if len(common_indices) > 0: 
            #filter out any values not in the common index and then sort data so they match indices 
            train_data_filtered = train_data[train_data[index].isin(common_indices)]
            prediction_data_filtered = prediction_data[prediction_data[index].isin(common_indices)]
            train_data_sorted = train_data_filtered.sort_values(by=index).reset_index(drop=True)
            prediction_data_sorted = prediction_data_filtered.sort_values(by=index).reset_index(drop=True)
            ground_truth = {"y_train": train_data_sorted[self._get_config("model_target")]}
            predictions = {"train": prediction_data_sorted["predictions"]}
          
            #get model object and calculate metrics
            model_version = self.metadata_tracker.get_prediction_job_model_version(prediction_job)
            experiment = self.metadata_tracker.get_winning_experiment(model_version)
            model_obj = self.resource_version_control.get_model(experiment)
            model = self.metadata_tracker.load_model(model_obj, model_version, None)
            metrics_val = model.calculate_metrics(ground_truth, predictions, self.train._get_config("metrics"))

            #log stuff
            self.metrics_tracker.log_metrics(prediction_job, metrics_val, self.train._get_config("perf_metric"))
            self.metrics_tracker.log_metric(prediction_job, "num_ground_truth_observations", train_data_sorted.shape[0])
        else: #nothing in prediction has a ground truth yet 
            self.notify("Current training data has no overlap with the prediction job %s" %self.metadata_tracker.get_resource_id(prediction_job), level = "WARNING")

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
    
