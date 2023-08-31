from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

import pandas as pd
from pathlib import Path 


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = { "components" : ["resource_version_control"], 
                         "config": ["transformer_path"]

    }


    __DEFAULT_CONF__ = {
        "config": {"transformer_func": "transform",
                   "fit_func": "fit",
                   "fit_params": {} 
                   }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        transformer_path = Path(self._get_config("feature_transformer_path"))
        fit_func = self._get_config("fit_func")
        self.params = self._get_config("fit_params")

        if transformer_path.exists():
            transformer = utils.load_plugin(transformer_path, self)

            self._fit = getattr(transformer, fit_func)
        else:
            self.log("Transformer path not found %s" % transformer_path)

    def fit(self, data, *args, **kwargs): 
        if not hasattr(self, "_fit"):
            raise Exception(
                "No feature transformer found. Unable to fit transformer.")
        
        self.transformer = self._fit(data, **self.params.update(kwargs))

        return self.transformer

    def transform(self, data, *args, **kwargs):

        if not hasattr(self, "transformer"): 
            raise Exception("No feature transformer found. Unable to transform features.")
        
        transformer = getattr(
            self.transformer, 
            self._get_config("transform_func")
            )
        data_out = transformer(data, **kwargs)

        return data_out 
    
    def fit_transform(self, data, *args, **kwargs): 
       
        self.fit(data, *args, **kwargs)

        data_out = self.transform(data, *args, **kwargs)

        return data_out  

    def save(self, experiment, *args, **kwargs):
        transformer = self.name 
        vc_info = self.resource_version_control.version_feature_transformer(experiment, self.transformer, algo=transformer)
        experiment_metadata = {
            "feature_transformer_fit_params" : self.params,
            "feature_transformer" : transformer
        }
        self.metadata_tracker.register_vc_resource(experiment, vc_info, additional_metadata = experiment_metadata)

    def load(self, source, *args, **kwargs):
        pass
