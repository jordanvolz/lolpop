from lolpop.pipeline.predict.base_predict import BasePredict
from lolpop.utils import common_utils as utils
from lolpop.utils import metaflow_utils as meta_utils
from metaflow import FlowSpec, step
from pathlib import Path

METAFLOW_CLASS = "MetaflowOfflinePredictSpec"
PLUGIN_PATHS = "plugin_paths.txt"

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowOfflinePredict(BasePredict):
    __REQUIRED_CONF__ = {
        "components": ["data_connector", "metadata_tracker", "resource_version_control", "model_explainer", "data_checker", "data_profiler"],
        "config": []
    }

    def run(self, model, model_version, data, dataset_version, **kwargs):
        #get flow class object from this file
        mod_cl = meta_utils.get_flow_class(__file__, METAFLOW_CLASS)

        flow = meta_utils.load_flow(
            mod_cl, self, PLUGIN_PATHS, model=model, model_version=model_version, 
            data=data, dataset_version=dataset_version)
        self.log("Loaded metaflow flow %s" % METAFLOW_CLASS)

        meta_utils.run_flow(flow, "run", __file__, PLUGIN_PATHS)
        self.log("Metaflow pipeline %s finished." % METAFLOW_CLASS)

    def get_artifacts(self, artifact_keys):
        #get latest run of this pipeline
        run = meta_utils.get_latest_run(METAFLOW_CLASS)

        #get requested artifacts
        artifacts = meta_utils.get_run_artifacts(
            run, artifact_keys, METAFLOW_CLASS)

        return artifacts


class MetaflowOfflinePredictSpec(FlowSpec):

    def __init__(self, lolpop=None, model=None, model_version=None, data = None, dataset_version = None, use_cli=False, **kwargs):
        #you need to set local attributes before calling super
        #only the first time we create the class will these parameters be provided.
        #The rest of the calls are metaflow internal calls and we do not want to reset them
        if lolpop is not None:
            self.lolpop = lolpop
        if model is not None:
            self.model = model
        if model_version is not None:
            self.model_version = model_version
        if data is not None: 
            self.data = data 
        if dataset_version is not None: 
            self.dataset_version = dataset_version

        #load plugins
        meta_utils.load_plugins(PLUGIN_PATHS)

        #call init -- this kicks off the main workflow
        super().__init__(use_cli=use_cli)

    @step
    def start(self):
        self.next(self.compare_data)

    @step
    def compare_data(self):
        #get training dataset version and df
        vc_info = self.lolpop.metadata_tracker.get_vc_info(
            self.model_version, key="X_train_hexsha")
        train_df = self.lolpop.resource_version_control.get_data(
            self.model_version, vc_info, key="X_train")

        #compare current dataset version with previous dataset version
        comparison_report, file_path = self.lolpop.data_profiler.compare_data(
            self.data, train_df)

        self.lolpop.metadata_tracker.log_data_comparison(
            self.dataset_version,
            file_path=file_path,
            report=comparison_report,
            profiler_class=self.lolpop.data_profiler.name
        )

        self.next(self.get_predictions)

    @step
    def get_predictions(self):
        #get prediction job
        prediction_id = "%s_predictions" % self.lolpop.metadata_tracker.get_resource_id(
            self.model_version)
        prediction_job = self.lolpop.metadata_tracker.create_resource(
            id=prediction_id, type="prediction_job", parent=self.model_version, prediction_count=self.data.shape[0])

        data = self.data
        #drop any metadata columns
        df = data.drop(self.lolpop._get_config("DROP_COLUMNS", []),
                       axis=1, errors="ignore")

        #make predictions
        data["predictions"] = self.model._predict_df(df)
        if self.lolpop.problem_type == "classification":
            data["predictions_proba"] = self.model._predict_proba_df(
                df, to_list=True)

        #get explanations
        data["explanations"] = self.lolpop.model_explainer.get_explanations(
            df, self.model, self.model_version, "predictions", to_list=True)

        #log predictions
        self.lolpop.metrics_tracker.log_prediction_metrics(
            prediction_job, data["predictions"])

        self.data = data 
        self.prediction_job = prediction_job

        self.next(self.track_predictions)

    @step
    def track_predictions(self):
        #version data
        vc_info = self.lolpop.resource_version_control.version_data(
            self.prediction_job, self.data)

        #register version control metadata w/ metadata tracker
        self.lolpop.metadata_tracker.register_vc_resource(
            self.prediction_job, vc_info, file_type="csv")
        
        self.next(self.analyze_prediction_drift)

    @step
    def analyze_prediction_drift(self):
        #get previous dataset version & dataframe
        prev_dataset_version = self.lolpop.metadata_tracker.get_prev_resource_version(
            self.dataset_version)
        if prev_dataset_version is not None:
            vc_info = self.lolpop.metadata_tracker.get_vc_info(prev_dataset_version)
            prev_data = self.lolpop.resource_version_control.get_data(
                prev_dataset_version, vc_info)

            #compare current dataset version with previous dataset version
            comparison_report, file_path = self.lolpop.data_profiler.compare_data(
                self.data, prev_data)

            self.lolpop.metadata_tracker.log_data_comparison(
                self.prediction_job,
                file_path=file_path,
                report=comparison_report,
                profiler_class=self.lolpop.data_profiler.name
            )

        self.next(self.check_predictions)

    @step
    def check_predictions(self):
        #run data checks
        data = self.data.drop(
            ["explanations", "predictions_proba"], axis=1, errors="ignore")
        data_report, file_path, checks_status = self.lolpop.data_checker.check_data(
            data)

        #log data report to metadata tracker
        self.lolpop.metadata_tracker.log_checks(
            self.prediction_job,
            file_path=file_path,
            report=data_report,
            checker_class=self.lolpop.data_checker.name,
            type="prediction"
        )

        if checks_status == "ERROR" or checks_status == "WARN":
            url = self.lolpop.metadata_tracker.url
            self.lolpop.notify(
                "Issues found with data checks. Visit %s for more information." % url, checks_status)
            
        self.next(self.save_predictions)

    @step
    def save_predictions(self):
        table = self.lolpop._get_config("prediction_data")
        self.lolpop.data_connector.save_data(self.data, table)

        self.next(self.end)

    @step
    def end(self): 
        pass


if __name__ == '__main__':
    #need to use CLI here because metaflow calls back into this function to
    #execute each individual step
    MetaflowOfflinePredictSpec(use_cli=True)
