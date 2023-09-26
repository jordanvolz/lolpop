from lolpop.component import LocalCacheManager
from tests.fixtures import *


class TestLocalCacheManager:

    def test_cache_data(self, simple_data, fake_component_config):
        path = LocalCacheManager(**fake_component_config).cache("test", simple_data)
        assert path.exists()

    def test_retrieve_data(self, simple_data, fake_component_config): 
        _ = LocalCacheManager(**fake_component_config).cache("test", simple_data)
        cached_data = LocalCacheManager(**fake_component_config).retrieve("test")
        assert cached_data.equals(simple_data)

    def test_compare_objects_pass(self, simple_data, fake_component_config): 
        data_copy = simple_data.copy()
        assert LocalCacheManager(**fake_component_config).equals(data_copy,simple_data)

    def test_compare_objects_fail(self, simple_data, fake_component_config): 
        data_copy = simple_data.copy()
        data_copy["new_col"]=100
        assert not LocalCacheManager(**fake_component_config).equals(data_copy,simple_data)