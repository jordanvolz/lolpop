from lolpop.component.feature_transformer.base_feature_transformer import BaseFeatureTransformer
from lolpop.utils import common_utils as utils

from sklearn.pipeline import Pipeline
from feature_engine import imputation, encoding, discretisation, outliers, transformation, creation, datetime, selection, preprocessing
from feature_engine.timeseries import forecasting   


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class FeatureEngineFeatureTransformer(BaseFeatureTransformer):
    __REQUIRED_CONF__ = {"config": ["transformers"]
                         }

    __DEFAULT_CONF__ = {
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
                list(t.get("transformer_columns")),
                *t.get("transformer_args",[]), 
                **t.get("transformer_kwargs",{})
                )
            name = "transform_%s" %i 
            i+=1 
            transformer_array.append((name, transformer))
        
        #now we can call ColumnTranformer on the transformer_array 
        self.params = self._get_config("pipeline_kwargs",{})
        self.transformer = Pipeline(transformer_array, **self.params)


    def fit(self, X_data, y_data=None, *args, **kwargs):
        """
        Fit the feature transformer to the data.

        Args:
            X_data (object): The input data to fit the transformer to.
            y_data (object): The target data.
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

        data_out = self.transformer.transform(data, **kwargs)

        return data_out
    
    def fit_transform(self, X_data, y_data=None, *args, **kwargs): 
        """
        Fit the feature transformer to the data and transform it.

        Args:
            X_data: The input data to fit the transformer to and transform.
            y_data: The target data. 
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

    def _get_transformer(self, transformer_class, columns, *args, **kwargs): 
        """
        Get the feature_engine transformer object based on the given class name.

        Args:
            transformer_class: The class name of the transformer.
            columns: list of columns to apply the transformer to 
            *args: Positional arguments to be passed to the transformer constructor.
            **kwargs: Keyword arguments to be passed to the transformer constructor.

        Returns:
            object: The instantiated scikit-learn transformer object.

        Raises:
            Exception: If there is an error loading the transformer from `sklearn.preprocessing`.

        """
        try: 
            transformer = self._map_transformer(transformer_class) 
            return transformer(variables=columns, *args, **kwargs)
        except Exception as e: 
            raise Exception("Error loading transformer %s from feature_engine." %transformer_class)
        
    def _map_transformer(self, transformer_class): 
        """
        Map the transformer class name to the corresponding feature_engine transformer object.

        Args:
            transformer_class (str): The class name of the transformer.

        Returns:
            object: The instantiated feature_engine transformer object.

        Raises:
            None

        """
        imputer_list = [
            "MeanMedianImputer", 
            "ArbitraryNumberImputer", 
            "EndTailImputer",
            "CategoricalImputer", 
            "RandomSampleImputer",
            "AddMissingIndicator",
            "DropMissingData"
        ]
        
        encoder_list = [
            "OneHotEncoder",
            "CountFrequencyEncoder",
            "OrdinalEncoder",
            "MeanEncoder",
            "WoEEncoder",
            "DecisionTreeEncoder",
            "RareLabelEncoder",
            "StringSimilarityEncoder",
        ]

        discretiser_list = [
            "ArbitraryDiscretiser",
            "EqualFrequencyDiscretiser",
            "EqualWidthDiscretiser",
            "DecisionTreeDiscretiser",
            "GeometricWidthDiscretiser",
        ]

        outlier_list = [
            "ArbitraryOutlierCapper",
            "Winsorizer",
            "OutlierTrimmer",
        ]

        numerical_list = [
            "LogTransformer",
            "LogCpTransformer",
            "ReciprocalTransformer",
            "PowerTransformer",
            "BoxCoxTransformer",
            "YeoJohnsonTransformer",
            "ArcsinTransformer",
        ]

        creation_list = [
            "MathFeatures",
            "RelativeFeatures",
            "CyclicalFeatures",
        ]

        datetime_list = [
            "DatetimeFeatures",
            "DatetimeSubtraction",
        ]

        selection_list = [
            "DropFeatures",
            "DropConstantFeatures",
            "DropDuplicateFeatures",
            "DropCorrelatedFeatures",
            "SmartCorrelatedSelection",
            "DropHighPSIFeatures",
            "SelectByInformationValue",
            "SelectByShuffling",
            "SelectBySingleFeaturePerformance",
            "SelectByTargetMeanPerformance",
            "RecursiveFeatureElimination",
            "RecursiveFeatureAddition",
            "ProbeFeatureSelection",
        ]

        forecasting_list = [
            "LagFeatures",
            "WindowFeatures",
            "ExpandingWindowFeatures",
        ]

        preprocessing_list = [
            "MatchCategories",
            "MatchVariables",
        ]

        transformer = None 

        if transformer_class in imputer_list:
            transformer = getattr(imputation, transformer_class)

        elif transformer_class in encoder_list: 
            transformer = getattr(encoding, transformer_class)

        elif transformer_class in discretiser_list: 
            transformer = getattr(discretisation, transformer_class)
        
        elif transformer_class in outlier_list: 
            transformer = getattr(outliers, transformer_class)

        elif transformer_class in numerical_list: 
            transformer = getattr(transformation, transformer_class)

        elif transformer_class in creation_list: 
            transformer = getattr(creation, transformer_class)

        elif transformer_class in datetime_list: 
            transformer = getattr(datetime, transformer_class)

        elif transformer_class in selection_list: 
            transformer = getattr(selection, transformer_class)

        elif transformer_class in forecasting_list:  
            transformer = getattr(forecasting, transformer_class)

        elif transformer_class in preprocessing_list: 
            transformer = getattr(preprocessing, transformer_class)

        else: 
            self.log("Transformer class %s not found!" %transformer_class, level="WARN")

        return transformer

