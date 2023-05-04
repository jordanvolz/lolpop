from lolpop.component.base_component import BaseComponent


class BaseDataSynthesizer(BaseComponent):

    def load_data(self, source_file, *args, **kwargs):
        pass

    def model_data(self, data, *args, **kwargs):
        pass

    def sample_data(self, model, num_rows, *args, **kwargs):
        pass

    def evaluate_data(self, real_data, synthetic_data, *args, **kwargs):
        pass
