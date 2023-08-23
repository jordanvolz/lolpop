from lolpop.component.model_visualizer.base_model_visualizer import BaseModelVisualizer
from lolpop.utils import common_utils as utils
from matplotlib import pyplot as plt 
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ProphetModelVisualizer(BaseModelVisualizer):

    __REQUIRED_CONF__ = {
        "components": ["metadata_tracker"],
    }

    def generate_viz(self, data, model, model_version, forecast_period=7, forecast_frequency="D", *args, **kwargs):
        """ Method to generate visualizations of Prophet model components and forecasts. 
    
        Args:
        
            data: pandas DataFrame
                Input DataFrame containing time-series data.
            model: Prophet model object
                A trained Prophet model object.
            model_version: object
                Model version from the metadata_tracker
            forecast_period: int, default 7
                The period for which forecast is to be generated.
            forecast_frequency: str, default 'D'
                The frequency of the forecast period.
        
        Returns:
        
            None
        """
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

    def cross_validation(self, model, model_version, initial, period, horizon, *args, **kwargs): 
        """Method to perform time-series cross validation on the Prophet model.
    
        Args:
        
            model: Prophet model object
                A trained Prophet model object.
            model_version: str
                String defining the model version.
            initial: str, int or float
                String or numerical value to define the size of the initial training period.
            period: str, int or float
                String or numerical value to define the length of the spacing between cutoff dates.
            horizon: str, int or float
                String or numerical value to define the forecast horizon.
        
        Returns:
        
            None
        """

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
        """Helper method to save plots generated by ProphetModelVisualizer methods to local directory and log them with the metadata tracker.
    
        Args:
        
            dir: str
                Directory path (String) for saving the file.
            id: str
                Unique identifier for the model version.
            file_name: str
                Name for the file to be saved.
            model_version: object
                model version to log file to 
        
        Returns:
        
            None
        
        """
        file_path = "%s/%s_%s" % (dir, id, file_name)
        plt.savefig(file_path)
        name = file_name.split(".")[0]
        if model_version is not None: 
            self.metadata_tracker.log_artifact(model_version, name, file_path)
        plt.close()
