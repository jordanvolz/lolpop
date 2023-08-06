from lolpop.component import EvidentlyAIDataChecker
from tests.fixtures import * 

class TestEvidentlyAIDataChecker:

    def test_check_data(self, simple_data, fake_component_config):
        _ = EvidentlyAIDataChecker(**fake_component_config).check_data(simple_data)
        assert 1

