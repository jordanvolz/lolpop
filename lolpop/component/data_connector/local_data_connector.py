from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalDataConnector(BaseDataConnector):

    __DEFAULT_CONF__ = {
        "config" : {"save_index": True}
    }

    def get_data(self, source_path, *args, **kwargs):
        """
        Reads a CSV, Parquet, or ORC file from a local storage and returns the data as a pandas DataFrame.

        Args:
            source_path (str): The path to the data source file.

        Returns:
            pandas.DataFrame: Returns data as a pandas DataFrame.
        """
        file_type = source_path.split(".")[-1]
        if file_type == "csv":
            data = pd.read_csv(source_path, engine="pyarrow", **kwargs)
        elif file_type == "parquet" or file_type == "pq":
            data = pd.read_parquet(source_path, engine="pyarrow", **kwargs)
        elif file_type == "orc":
            data = pd.read_orc(source_path, engine="pyarrow", **kwargs)
        else: 
            self.log("Unsupported file type provided: %s" %source_path)
        self.log("Successfully loaded data from %s into DataFrame." %source_path)

        return data 

    def save_data(self, data, target_path, save_index=None, *args, **kwargs):
        """
        Writes a CSV or Parquet file to a local storage and returns the saved data.

        Args:
            data (pandas.DataFrame): Data to be saved.
            target_path (str): The path to the target file.

        Returns:
            pandas.DataFrame: Returns saved data.
        """
        if save_index is None: 
            save_index = self._get_config("save_index")
        file_type = target_path.split(".")[-1]
        if file_type == "csv":
            data = data.to_csv(target_path, index=save_index, **kwargs)
        elif file_type == "parquet" or file_type == "pq":
            data = data.to_parquet(target_path, index=save_index, **kwargs)
        self.log("Successfully saved data to %s." %target_path)
        return data
