from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

from sklearn import preprocessing
from sklearn.compose import ColumnTransformer


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class sklearnFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = {"components": ["resource_version_control"],
                         "config": ["transformers"]

                         }

    __DEFAULT_CONF__ = {
        "config": {"column_transformer_kwargs": {}}
    }

#transformers: [{
# transformer: 
# transformer_columns: 
# transformer_kwargs: 
# transformer_args:
# },
#..
#]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #get transformer config and process
        transformers = self._get_config("transformers",[])
        i = 1
        transformer_array = []
        for t in transformers: 
            transformer = self._get_transformer(
                t.get("transformer"),
                *t.get("transformer_args",[]), 
                **t.get("transformer_kwargs",{})
                )
            name = "transform_%s" %i 
            columns = list(t.get("transformer_columns"))
            i+=1 
            transformer_array.append((name, transformer, columns))
        
        #now we can call ColumnTranformer on the transformer_array 
        self.transformer = ColumnTransformer(transformers=transformer_array)
        self.params = self._get_config("column_transformer_kwargs")


    def fit(self, data, *args, **kwargs):
        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to fit transformer.")
        if kwargs is not None: 
            self.params.update(kwargs)
        self.transformer = self.transformer.fit(data, **self.params)

        return self.transformer

    def transform(self, data, *args, **kwargs):

        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to transform features.")

        data_out = self.transformer.transform(data, **kwargs)

        return data_out
    
    def fit_transform(self, data, *args, **kwargs): 
        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to transform features.")

        data_out = self.transformer.fit_transform(data, **kwargs)

        return data_out

    def save(self, experiment, *args, **kwargs):
        transformer = self.name
        vc_info = self.resource_version_control.version_feature_transformer(
            experiment, self.transformer, algo=transformer)
        experiment_metadata = {
            "feature_transformer_fit_params": self.params,
            "feature_transformer": transformer
        }
        self.metadata_tracker.register_vc_resource(
            experiment, vc_info, additional_metadata=experiment_metadata)

    def load(self, source, *args, **kwargs):
        pass

    def _get_transformer(self, transformer_class, *args, **kwargs): 
        try: 
            transformer = getattr(preprocessing, transformer_class)
            return transformer(*args, **kwargs)
        except Exception as e: 
            raise Exception("Error loading transformer %s from sklearn.preprocessing." %transformer_class)