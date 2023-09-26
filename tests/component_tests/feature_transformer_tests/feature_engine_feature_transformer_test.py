from lolpop.component import FeatureEngineFeatureTransformer
from lolpop.utils import common_utils as utils
from tests.fixtures import *


class TestFeatureEngineFeatureTranformer:

    def test_fit_data(self, simple_data, fake_component_config):
        config = self._get_config(fake_component_config)
        _ = FeatureEngineFeatureTransformer(
            **config).fit(simple_data)
        assert 1

    def test_fit_transform_data(self, simple_data, fake_component_config):
        config = self._get_config(fake_component_config)
        _ = FeatureEngineFeatureTransformer(
            **config).fit_transform(simple_data)
        assert 1

    def test_transform_data(self, simple_data, fake_component_config):
        config = self._get_config(fake_component_config)
        _ = FeatureEngineFeatureTransformer(
            **config).fit(simple_data).transform(simple_data)
        assert 1

    def _get_config(self, config):
        config["conf"]["config"]["transformers"] = [
            {"transformer": "OneHotEncoder",
                "transformer_columns": ["state"]},
           	{"transformer": "LogCpTransformer", "transformer_columns": [
                    "some_float", "some_int"]},
        ]
        return config
