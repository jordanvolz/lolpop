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

    def process_data(self):
        #run data transformations and encodings
        data = self.process.transform_data()  # maybe better called get_training_data?

        #track & version data
        dataset_version = self.process.track_data(
            data, self.config.get("table_train"))

        #profile data
        self.process.profile_data(data, dataset_version)

        #run data checks
        self.process.check_data(data, dataset_version)

        #run data comparison/drift
        self.process.compare_data(data, dataset_version)

        #return data
        return data

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

        return model_version, is_new_model_better

    def deploy_model(self, model_version):
        #promote model
        promotion = self.deploy.promote_model(model_version)

        #check if model is approved
        is_approved = self.deploy.check_approval(promotion)

        #if approved, deploy model
        if is_approved:
            deployment = self.deploy.deploy_model(promotion, model_version)

        return deployment

    def predict_data(self, model, data):
        pass

    def build_all():
        pass
