from lolpop.component import DeepchecksDataChecker
from tests.fixtures import * 

class TestDeepchecksDataChecker:

    def test_check_data(self, simple_data, fake_component_config):
        _ = DeepchecksDataChecker(**fake_component_config).check_data(simple_data)
        assert 1

