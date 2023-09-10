from lolpop.component.base_component import BaseComponent
from typing import Any


class BaseFeatureTransformer(BaseComponent):
    __REQUIRED_CONF__ = {"components": ["resource_version_control", "metadata_tracker"]
                         }
    
    def fit(self, data, *args, **kwargs) -> Any: 
        pass 

    def transform(self, data, *args, **kwargs) -> Any:
        pass

    def fit_transform(self, data, *args, **kwargs) -> Any: 
        pass 

    def save(self, experiment, *args, **kwargs):
        """
        Saves the feature transformer and associated metadata using the resource version control.

        Args:
            experiment: The experiment associated with the feature transformer.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None.
        """
        transformer_class = self.name
        vc_info = self.resource_version_control.version_feature_transformer(
            experiment, self.transformer, transformer_class=transformer_class)
        experiment_metadata = {
            "feature_transformer_config": self.config,
            "feature_transformer_class": transformer_class
        }
        self.metadata_tracker.register_vc_resource(
            experiment, vc_info, key="feature_transformer", additional_metadata=experiment_metadata)

    def load(self, source, *args, **kwargs) -> Any:
        pass

    def _get_transformer(self) -> Any: 
        return self.transformer
    
    def _set_transformer(self, transformer): 
        self.transformer = transformer

