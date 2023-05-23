from lolpop.runner.base_runner import BaseRunner
from lolpop.utils import common_utils as utils


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class QuickstartRunner(BaseRunner):

    __REQUIRED_CONF__ = {
        "pipelines": ["process", "train", "predict"],
        "components": ["metadata_tracker", "metrics_tracker"],
        "config": ["train_data", "eval_data", "prediction_data", "model_target", "drop_columns"]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(problem_type="classification", *args, **kwargs)

    def process_data(self, source_data="train"):
        #run data transformations and encodings
        source_data_name = self._get_config("%s_data" % source_data)
        # maybe better called get_training_data?
        data = self.process.transform_data(source_data_name)

        return data

    def train_model(self, data):

        #split data
        data_dict = self.train.split_data(data)

        #train a model
        model, model_version = self.train.train_model(data_dict)

        return model, model_version 

    def predict_data(self, model, model_version, data):

        data, prediction_job = self.predict.get_predictions(
            model, model_version, data)


        return data, prediction_job


    def stop(self):
        self.metadata_tracker.stop()
        pass
