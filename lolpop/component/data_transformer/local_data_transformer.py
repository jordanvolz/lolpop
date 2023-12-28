from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils

from pathlib import Path 
from omegaconf import dictconfig


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalDataTransformer(BaseDataTransformer):

    __REQUIRED_CONF__ = {
        "config": ["transformer_path"]
    }

    __DEFAULT_CONF__ = {
        "config": {"transformer_func": "transform", 
                   "data_connector": "LocalDataConnector"}
    }

    def __init__(self, dependent_integrations=None, *args, **kwargs):
        if dependent_integrations is None: 
            dependent_integrations = {}
            
        super().__init__(dependent_integrations=dependent_integrations, *args, **kwargs)

        transformer_path = Path(self._get_config("transformer_path")) 
        transformer_func = self._get_config("transformer_func")
        
        if transformer_path.exists(): 
            transformer = utils.load_plugin(transformer_path, self)

            self._transform = getattr(transformer, transformer_func)
        else: 
            self.log("Transformer path not found %s" %transformer_path)

        #load data connector
        data_connector_cl_name=self._get_config("data_connector")
        data_connector_config = self._get_config(
            "data_connector_config", {})
        data_connector_cl = utils.load_class(data_connector_cl_name)
        data_connector = data_connector_cl(
            conf = {"config": data_connector_config},
            parent=self,
            is_standalone=True,
            dependent_integrations={"component": {"logger": self.logger, "notifier": self.notifier, "metadata_tracker": self.metadata_tracker}}
            )       
        self.data_connector = data_connector

    def transform(self, input_data, *args, **kwargs):
        """Runs local transformer workflow in python.

        Args:
            input_data (String): Names of file to load and pass to transformer file.

        Returns:
            pd.DataFrame: the transformed data
        """
        if isinstance(input_data,dict) or isinstance(input_data, dictconfig.DictConfig): 
            data = {k: self.data_connector.get_data(v) for k,v in input_data.items()}
        elif isinstance(input_data,str): 
            data = self.data_connector.get_data(input_data)
        else: 
            raise Exception("input_data not a valid type. Expecting dict or str. Found: %s" %str(type(input_data)))
        kwargs = self._get_config("transformer_kwargs",{})

        data_out = self._transform(data, **kwargs)

        return data_out
