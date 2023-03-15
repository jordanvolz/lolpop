from lolpop.component import YDataProfilingDataProfiler
from lolpop.utils import common_utils as utils
from tests.fixtures import *


class TestYDataProfilingDataProfiler:

    def test_profile_data(self, simple_data, fake_component_config):
        _ = YDataProfilingDataProfiler(
            **fake_component_config).profile_data(simple_data)
        assert 1

    def test_compare_data(self, simple_data, fake_component_config):
        _ = YDataProfilingDataProfiler(
            **fake_component_config).compare_data(simple_data, simple_data[:1000])
        assert 1
