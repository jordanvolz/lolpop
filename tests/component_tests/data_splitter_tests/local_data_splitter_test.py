from lolpop.component import LocalDataSplitter
from lolpop.utils import common_utils as utils
from tests.fixtures import *


class TestEvidentlyAIDataProfiler:

    def test_config(self, fake_component_config):
        try:
            _ = LocalDataSplitter(**fake_component_config)
            assert 0
        except:
            assert 1

    def test_split_data_default(self, simple_data, fake_component_config):
        fake_component_config["config"]["config"]["model_target"] = simple_data.columns[0]
        fake_component_config["config"]["config"]["drop_columns"] = [
            simple_data.columns[1], simple_data.columns[2]]
        out = LocalDataSplitter(
            **fake_component_config).split_data(simple_data)
        assert len(out) == 4

    def test_split_data_with_test(self, simple_data, fake_component_config):
        fake_component_config["config"]["config"]["model_target"] = simple_data.columns[0]
        fake_component_config["config"]["config"]["drop_columns"] = [
            simple_data.columns[1], simple_data.columns[2]]
        fake_component_config["config"]["config"]["include_test"] = True
        fake_component_config["config"]["config"]["split_ratio"] = [0.8,0.1,0.1]
        out = LocalDataSplitter(
            **fake_component_config).split_data(simple_data)
        assert len(out) == 6

    def test_split_data_sample(self, simple_data, fake_component_config):
        fake_component_config["config"]["config"]["model_target"] = simple_data.columns[0]
        fake_component_config["config"]["config"]["drop_columns"] = [
            simple_data.columns[1], simple_data.columns[2]]
        fake_component_config["config"]["config"]["sample_num"] = 100
        out = LocalDataSplitter(
            **fake_component_config).split_data(simple_data)
        assert (out.get("X_train").shape[0] + out.get("X_valid").shape[0]==100)

    def test_split_data_manual(self, simple_data, fake_component_config):
        fake_component_config["config"]["config"]["model_target"] = simple_data.columns[0]
        fake_component_config["config"]["config"]["drop_columns"] = [
            simple_data.columns[1], simple_data.columns[2]]
        fake_component_config["config"]["config"]["split_column"] = "some_bool"
        fake_component_config["config"]["config"]["split_classes"] = {"train": True, "valid": False}
        out = LocalDataSplitter(
            **fake_component_config).split_data(simple_data)
        assert 1

    def test_split_data_stratified(self, simple_data, fake_component_config):
        fake_component_config["config"]["config"]["model_target"] = "some_bool"
        fake_component_config["config"]["config"]["drop_columns"] = [
            simple_data.columns[1], simple_data.columns[2]]
        fake_component_config["config"]["config"]["use_stratified"] = True
        out = LocalDataSplitter(
            **fake_component_config).split_data(simple_data)
        assert 1
