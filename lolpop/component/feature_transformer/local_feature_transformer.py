from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

import pandas as pd
from pathlib import Path 


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = {"config": ["feature_transformer_path"]

    }

    __DEFAULT_CONF__ = {
        "config": {"transform_func": "transform",
                   "fit_func": "fit",
                   "fit_params": {}, 
                   "transform_params": {},
                   }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        transformer_path = Path(self._get_config("feature_transformer_path"))
        fit_func = self._get_config("fit_func")
        self.params = self._get_config("fit_params",{})

        if transformer_path.exists():
            transformer = utils.load_plugin(transformer_path, self)

            self._fit = getattr(transformer, fit_func)
        else:
            self.log("Transformer path not found %s" % transformer_path)

    def fit(self, data, *args, **kwargs): 
        """
        Fits the feature transformer with the given data.

        Args:
            data: The input data to fit the transformer.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The fitted feature transformer.

        Raises:
            Exception: If no feature transformer is found, unable to fit the transformer.
        """
        if not hasattr(self, "_fit"):
            raise Exception(
                "No feature transformer found. Unable to fit transformer.")
        if kwargs is not None:
            self.params.update(kwargs)
        self.transformer = self._fit(data, **self.params)

        return self.transformer

    def transform(self, data, *args, **kwargs):
        """
        Transforms the given data using the fitted feature transformer.

        Args:
            data: The input data to transform.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The transformed data.

        Raises:
            Exception: If no feature transformer is found, unable to transform features.
        """

        if not hasattr(self, "transformer"): 
            raise Exception("No feature transformer found. Unable to transform features.")
        
        transformer = getattr(
            self.transformer, 
            self._get_config("transform_func")
            )
        if kwargs is not None:
            self._get_config("transform_params", {}).update(kwargs)
        data_out = transformer(data, **kwargs)

        return data_out 
    
    def fit_transform(self, data, *args, **kwargs): 
        """
        Fits the feature transformer with the given data and then transforms the data.

        Args:
            data: The input data to fit and transform.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The transformed data.

        Raises:
            Exception: If no feature transformer is found, unable to fit or transform.
        """
        self.fit(data, *args, **kwargs)

        data_out = self.transform(data, *args, **kwargs)

        return data_out  
