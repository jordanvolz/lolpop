from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

from sklearn import preprocessing
from sklearn.compose import ColumnTransformer


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class sklearnFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = {"components": ["resource_version_control", "metadata_tracker"],
                         "config": ["transformers"]

                         }

    __DEFAULT_CONF__ = {
        "config": {"column_transformer_kwargs": {}}
    }

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
        """
        Fit the feature transformer to the data.

        Args:
            data: The input data to fit the transformer to.
            *args: Positional arguments to be passed to the `fit` method.
            **kwargs: Keyword arguments to be passed to the `fit` method.

        Returns:
            ColumnTransformer: The fitted ColumnTransformer object.

        Raises:
            Exception: If no feature transformer is found.

        """
        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to fit transformer.")
        if kwargs is not None: 
            self.params.update(kwargs)
        self.transformer = self.transformer.fit(data, **self.params)

        return self.transformer

    def transform(self, data, *args, **kwargs):
        """
        Apply the fitted feature transformer to transform the input data.

        Args:
            data: The input data to be transformed.
            *args: Positional arguments to be passed to the `transform` method.
            **kwargs: Keyword arguments to be passed to the `transform` method.

        Returns:
            numpy.ndarray or scipy.sparse matrix: The transformed data.

        Raises:
            Exception: If no feature transformer is found.

        """
        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to transform features.")

        data_out = self.transformer.transform(data, **kwargs)

        return data_out
    
    def fit_transform(self, data, *args, **kwargs): 
        """
        Fit the feature transformer to the data and transform it.

        Args:
            data: The input data to fit the transformer to and transform.
            *args: Positional arguments to be passed to the `fit_transform` method.
            **kwargs: Keyword arguments to be passed to the `fit_transform` method.

        Returns:
            numpy.ndarray or scipy.sparse matrix: The transformed data.

        Raises:
            Exception: If no feature transformer is found.

        """
        if not hasattr(self, "transformer"):
            raise Exception(
                "No feature transformer found. Unable to transform features.")

        data_out = self.transformer.fit_transform(data, **kwargs)

        return data_out

    def save(self, experiment, *args, **kwargs):
        """
        Save the feature transformer to a version control system.

        Args:
            experiment: The experiment object or identifier.
            *args: Positional arguments to be passed to the `version_feature_transformer` method.
            **kwargs: Keyword arguments to be passed to the `version_feature_transformer` method.

        """
        transformer = self.name
        vc_info = self.resource_version_control.version_feature_transformer(
            experiment, self.transformer, algo=transformer)
        experiment_metadata = {
            "feature_transformer_fit_params": self.params,
            "feature_transformer": transformer
        }
        self.metadata_tracker.register_vc_resource(
            experiment, vc_info, additional_metadata=experiment_metadata)

    def _get_transformer(self, transformer_class, *args, **kwargs): 
        """
        Get the scikit-learn transformer object based on the given class name.

        Args:
            transformer_class: The class name of the transformer.
            *args: Positional arguments to be passed to the transformer constructor.
            **kwargs: Keyword arguments to be passed to the transformer constructor.

        Returns:
            object: The instantiated scikit-learn transformer object.

        Raises:
            Exception: If there is an error loading the transformer from `sklearn.preprocessing`.

        """
        try: 
            transformer = getattr(preprocessing, transformer_class)
            return transformer(*args, **kwargs)
        except Exception as e: 
            raise Exception("Error loading transformer %s from sklearn.preprocessing." %transformer_class)