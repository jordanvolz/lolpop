from lolpop.component import LocalFeatureTransformer
from lolpop.utils import common_utils as utils
from tests.fixtures import *
from pathlib import Path 


class TestFeatureEngineFeatureTranformer:

    def test_fit_data(self, simple_data, fake_component_config):
        config = self._get_config(fake_component_config)
        _ = LocalFeatureTransformer(
            **config).fit(simple_data)
        assert 1

    def test_fit_transform_data(self, simple_data, fake_component_config):
        config = self._get_config(fake_component_config)
        _ = LocalFeatureTransformer(
            **config).fit_transform(simple_data)
        assert 1

    def test_transform_data(self, simple_data, fake_component_config):
        config = self._get_config(fake_component_config)
        ft = LocalFeatureTransformer(**config)
        ft.fit(simple_data)
        ft.transform(simple_data)
        assert 1

    def _get_config(self, config):
        transformer_path = Path(__file__).parent.resolve() / "files" / "my_transformer.py"
        config["conf"]["config"].update({
            "feature_transformer_path": transformer_path,
            "transformer_class": "MyTransformer",
            "categorical_columns": ["state"],
        })
        return config
