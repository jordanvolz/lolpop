from lolpop.component.model_visualizer.base_model_visualizer import BaseModelVisualizer
from lolpop.utils import common_utils as utils
from yellowbrick.classifier import ClassificationReport, ConfusionMatrix, ROCAUC, PrecisionRecallCurve, DiscriminationThreshold, ClassPredictionError
from yellowbrick.target import ClassBalance, FeatureCorrelation
import os 
from matplotlib import pyplot as plt
import matplotlib 
matplotlib.use('Agg')

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class YellowbrickModelVisualizer(BaseModelVisualizer): 

    def generate_viz(self, data, model, model_version): 
        
        if self.problem_type == "classification":
            classification_type = utils.get_multiclass(data["y_train"])
            #model = model._get_model() 

            #generate chart for each data split
            #this way is a little inefficient because we have to keep refitting viz
            #but the viz object seems to not allow re-using pyplot. This was the only way 
            #to get all plots to show -- by recreating the object for each split
            for split in set([x.split("_")[1] for x in data.keys()]): 
                #metric report
                viz = ClassificationReport(model)
                self._save_plot(viz, data, split, model_version, "yb_classification_report")

                #confusion matrix
                viz = ConfusionMatrix(model)
                self._save_plot(viz, data, split, model_version, "yb_confusion_matrix")

                #rocauc
                viz = ROCAUC(model)
                self._save_plot(viz, data, split, model_version, "yb_rocauc")

                #comment out for now -- errors if not all classes are represented in the predictions
                ##pr curve
                #viz = PrecisionRecallCurve(model, per_class=True) #per class handles multiclass use cases
                #self._save_plot(viz, data, split, model_version, "yb_prauc")

                #class error
                viz = ClassPredictionError(model)
                self._save_plot(viz, data, split, model_version, "yp_class_error")

                if classification_type == "binary":
                    #discrimination threshold -- only works for binary
                    viz = DiscriminationThreshold(model) 
                    self._save_plot(viz, data, split, model_version, "yb_disctreshold")

            #class balance
            viz = ClassBalance()
            viz.fit(data["y_train"])
            self._save_pyplot("yb_class_balance", "train", model_version)

            #class balance
            viz = FeatureCorrelation(labels=data["X_train"].columns)
            viz.fit(data["X_train"],data["y_train"])
            self._save_pyplot("yb_feature_correlation", "train", model_version)

            #note: could be fun to add some model selection viz here as well: https://www.scikit-yb.org/en/latest/api/model_selection/index.html
            # and yb has some interesting feature analysis viz that we could use in data processing: https://www.scikit-yb.org/en/latest/api/features/index.html

    def _save_plot(self, viz, data, split, model_version, plot_name): 
        viz.fit(data["X_train"], data["y_train"])
        viz.score(data["X_%s" %split], data["y_%s" %split])
        self._save_pyplot(plot_name, split, model_version)

    def _save_pyplot(self, name, label, model_version): 
        local_path = "%s/%s/%s" %(self._get_config("local_dir"), self.metadata_tracker.get_resource_id(model_version), label)
        os.makedirs(local_path, exist_ok=True)
        key = "%s_%s"%(name, label)
        local_file = "%s/%s.png" %(local_path, key)
        plt.savefig(local_file)
        artifact = self.metadata_tracker.log_artifact(model_version, id = key, path = local_file, external=False)
        #plt.clf()
        plt.close()

        return artifact
