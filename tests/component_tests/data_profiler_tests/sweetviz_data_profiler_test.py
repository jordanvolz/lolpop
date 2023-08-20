from lolpop.component import SweetvizDataProfiler
from lolpop.utils import common_utils as utils
from tests.fixtures import *


class TestSweetvizDataProfiler:

    def test_config(self, fake_component_config): 
        try: 
            _ = SweetvizDataProfiler(**fake_component_config)
            assert 0 
        except: 
            assert 1

    def test_profile_data(self, simple_data, fake_component_config):
        fake_component_config["conf"]["config"]["model_target"]=simple_data.columns[0]
        _ = SweetvizDataProfiler(
            **fake_component_config).profile_data(simple_data)
        assert 1

    def test_compare_data(self, simple_data, fake_component_config):
        fake_component_config["conf"]["config"]["model_target"] = simple_data.columns[0]
        _ = SweetvizDataProfiler(
            **fake_component_config).compare_data(simple_data, simple_data[:1000])
        assert 1
