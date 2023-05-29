from lolpop.component.model_visualizer.base_model_visualizer import BaseModelVisualizer
from lolpop.utils import common_utils as utils
from matplotlib import pyplot as plt 
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ProphetVisualizer(BaseModelVisualizer):

    def generate_viz(self, data, model, model_version, forecast_period=7, forecast_frequency="D"):

        # generate component plot
        id = self.metadata_tracker.get_resource_id(model_version)
        historic_predictions = model.predict(model.history)
        model.plot_components(historic_predictions)
        local_dir = self._get_config("local_dir")
        self._save_and_log_file(local_dir, id, "component_plot.png", model_version)

        #plot forecast
        future = model.make_future_dataframe(
            periods=forecast_period,
            freq=forecast_frequency,
            include_history=True
        )
        predictions = model.predict(future)
        model.plot(predictions)
        self._save_and_log_file(local_dir, id, "forecast_plot.png", model_version)

    def cross_validation(self, model, model_version, initial, period, horizon): 

        id = self.metadata_tracker.get_resource_id(model_version)
        df_cv = cross_validation(
            model,
            initial=initial,
            period=period,
            horizon=horizon,
        )

        df_p = performance_metrics(df_cv)

        #save performance metrics
        local_dir = self._get_config("local_dir")
        file_path = "%s/%s_%s" %(local_dir, id, "cv_performance_metrics.csv")
        df_p.to_csv(file_path)
        self.metadata_tracker.log_artifact(model_version, "cv_performance_metrics", file_path)

        #save plots
        for metric in df_p.drop(["horizon"], axis=1, errors="ignore"): 
            try: 
                plot_cross_validation_metric(df_cv, metric=metric)
                self._save_and_log_file(local_dir, id, "cv_performance_%s.png" % metric, model_version)
            except: 
                pass 
                

        
    def _save_and_log_file(self, dir, id, file_name, model_version): 
        file_path = "%s/%s_%s" % (dir, id, file_name)
        plt.savefig(file_path)
        name = file_name.split(".")[0]
        if model_version is not None: 
            self.metadata_tracker.log_artifact(model_version, name, file_path)
