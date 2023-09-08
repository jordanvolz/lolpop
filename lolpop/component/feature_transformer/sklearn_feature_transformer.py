from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

from sklearn import preprocessing
from sklearn.compose import ColumnTransformer

import numpy as np 
import pandas as pd 

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class sklearnFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = {"config": ["transformers"]
                         }

    __DEFAULT_CONF__ = {
        "config": {"column_transformer_kwargs": {"remainder": "passthrough", "verbose_feature_names_out": False}}
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
        self.params = self._get_config("column_transformer_kwargs")
        self.transformer = ColumnTransformer(transformers=transformer_array, **self.params)


    def fit(self, X_data, y_data=None, *args, **kwargs):
        """
        Fit the feature transformer to the data.

        Args:
            X_data: The input data to fit the transformer to.
            y_data: The label data. 
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
        self.transformer = self.transformer.fit(X_data, y_data, **kwargs)

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

        #transform data
        transform_out = self.transformer.transform(data, **kwargs)

        #make sure outpt is array-like
        if not isinstance(transform_out, np.ndarray): 
            transform_out = transform_out.toarray() 

        #convert to DF w/ correct column names
        data_out = pd.DataFrame(transform_out, columns=self.transformer.get_feature_names_out())

        return data_out
    
    def fit_transform(self, X_data, y_data=None, *args, **kwargs): 
        """
        Fit the feature transformer to the data and transform it.

        Args:
            X_data: The input data to fit the transformer to and transform.
            y_data: The label data. 
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

        data_out = self.transformer.fit_transform(X_data, y_data, **kwargs)

        return data_out

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