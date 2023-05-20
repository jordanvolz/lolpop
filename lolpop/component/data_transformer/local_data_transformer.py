from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.component.data_connector.local_data_connector import LocalDataConnector
from lolpop.utils import common_utils as utils

from pathlib import Path 
from omegaconf import dictconfig


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalDataTransformer(BaseDataTransformer):

    #use load_config to allow setting "DBT_TARGET", "DBT_PROFILE", "DBT_PROJECT_DIR", "DBT_PROFILES_DIR",  via env variables
    __REQUIRED_CONF__ = {
        "config": ["transformer_path"]
    }

    def __init__(self, components={}, *args, **kwargs):
        super().__init__(components=components, *args, **kwargs)

        transformer_path = Path(self._get_config("transformer_path")) 
        transformer_func = self._get_config("transformer_func", "transform")
        
        if transformer_path.exists(): 
            transformer = utils.load_plugin(transformer_path, self)

            self._transform = getattr(transformer, transformer_func)
        else: 
            self.log("Transformer path not found %s" %transformer_path)

        #load data connector
        data_connector_cl_name=self._get_config("data_connector", "LocalDataConnector")
        data_connector_config = self._get_config(
            "data_connector_config", {})
        data_connector_cl = utils.load_class(data_connector_cl_name)
        data_connector = data_connector_cl(
            conf = data_connector_config, pipeline_conf = {}, runner_conf = {}, 
            components={"logger": self.logger})
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
