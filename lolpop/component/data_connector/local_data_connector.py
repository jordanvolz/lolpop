from lolpop.component.data_connector.base_data_connector import BaseDataConnector
from lolpop.utils import common_utils as utils

import pandas as pd

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LocalDataConnector(BaseDataConnector):

    def get_data(self, source_path, *args, **kwargs):
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

    def save_data(self, data, target_path, *args, **kwargs):
        file_type = target_path.split(".")[-1]
        if file_type == "csv":
            data = data.to_csv(target_path, **kwargs)
        elif file_type == "parquet" or file_type == "pq":
            data = data.to_parquet(target_path, **kwargs)
        self.log("Successfully saved data to %s." %target_path)
        return data
