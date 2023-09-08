from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

from pathlib import Path 


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = {"config": ["feature_transformer_path", "transformer_class"]

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
        self.params = self._get_config("fit_params",{})

        if transformer_path.exists():
            transformer = utils.load_plugin(transformer_path, self)

            transformer_class = self._get_config("transformer_class")
            transformer_cl = getattr(transformer, self._get_config("transformer_class"))
            self.transformer = transformer_cl()
            self.log("Successfully loaded local transformer %s" %transformer_class)
        else:
            self.log("Transformer path not found %s" % transformer_path)

    def fit(self, X_data, y_data=None, *args, **kwargs): 
        """
        Fits the feature transformer with the given data.

        Args:
            X_data: The input data to fit the transformer.
            y_data: the label data. 
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The fitted feature transformer.

        Raises:
            Exception: If no feature transformer is found, unable to fit the transformer.
        """
        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to fit transformer.")
        if kwargs is not None:
            self.params.update(kwargs)

        fit_func = self._get_config("fit_func")
        if hasattr(self.transformer, fit_func): 
            fit_transformer = getattr(self.transformer, fit_func)
            fit_transformer(self.config, X_data, y_data, **self.params)
        else: 
            self.notify("Unable to find fit function %s for transformer %s" %(fit_func, self._get_config("transformer_class")))

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
        if kwargs is not None:
            self._get_config("transform_params", {}).update(kwargs)

        transform_func = self._get_config("transform_func")
        if hasattr(self.transformer, transform_func):
            transform = getattr(self.transformer, transform_func)

            data_out = transform(self.config, data, **kwargs)
            
        else: 
            raise Exception("Unable to find transform function %s for transformer %s" % (
                transform_func, self._get_config("transformer_class")))

        return data_out 
    
    def fit_transform(self, X_data, y_data = None, *args, **kwargs): 
        """
        Fits the feature transformer with the given data and then transforms the data.

        Args:
            X_data: The input data to fit and transform.
            y_data: The label data. 
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The transformed data.

        Raises:
            Exception: If no feature transformer is found, unable to fit or transform.
        """
        self.fit(X_data, y_data, *args, **kwargs)

        data_out = self.transform(X_data, *args, **kwargs)

        return data_out  
