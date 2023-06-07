from lolpop.component import StumpyMatrixProfiler
from tests.fixtures import *
import numpy as np
from matplotlib import pyplot as plt

class TestStumpyMatrixProfiler: 

    def test_config(self, fake_component_config):
        try:
            _ = StumpyMatrixProfiler(**fake_component_config)
            assert 0
        except:
            assert 1

    def test_check_data(self,simple_ts_data, fake_component_config):
        config = self.get_config(fake_component_config, simple_ts_data)
        smp = StumpyMatrixProfiler(**config)
        _ = smp.check_data(simple_ts_data)
        assert 1

    def test__plot_mp(self, fake_component_config, simple_ts_data):
        # Test case 1: Single plot
        axs = plt.subplots(2)[1]
        m = 5
        h = 10
        mp = np.random.rand(50, 1)
        discords = [6, 7, 8]
        i = 1
        config = self.get_config(fake_component_config, simple_ts_data)
        smp = StumpyMatrixProfiler(**config)
        smp._plot_mp(axs, m, h, mp, discords, i)
        assert isinstance(axs[i], plt.Axes)
        assert len(axs[i].get_lines()) == 4
        assert len(axs[i].collections) == 0
        assert len(axs[i].patches) == 3

    def test__plot_mp_mult(self, fake_component_config, simple_ts_data):
        # Test case 2: Multiple plots
        axs = plt.subplots(4)[1]
        m = 3
        h = 5
        mp = np.random.rand(50, 1)
        discords = [0, 1, 2]
        i = 1
        config = self.get_config(fake_component_config, simple_ts_data)
        smp = StumpyMatrixProfiler(**config)
        smp._plot_mp(axs, m, h, mp, discords, i)
        m=4
        i=2
        smp._plot_mp(axs, m, h, mp, discords, i)
        assert isinstance(axs[i], plt.Axes)
        assert len(axs[i].get_lines()) == 4
        assert len(axs[i].collections) == 0
        assert len(axs[i].patches) == 3

    def get_config(self, config, data):
        config["conf"]["config"]["model_target"] = data.columns[1]
        return config 
