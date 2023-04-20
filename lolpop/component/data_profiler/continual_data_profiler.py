from lolpop.component.data_profiler.base_data_profiler import BaseDataProfiler
from lolpop.utils import common_utils as utils

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class ContinualDataProfiler(BaseDataProfiler): 

    def profile_data(self, data, entry_names=["train"], datetime_columns=[], index_column=None, time_index_column=None, **kwargs): 
        #bit of a hack as this function currently requires an index
        if index_column is None: 
            index_column = self._get_config("model_index") or "ID"
            if "ID" not in data.columns: 
                data["ID"]=data.index
            
        if time_index_column is None: 
            time_index_column = self._get_config("model_time_index") or None 

        if len(datetime_columns) == 0: 
            datetime_columns = self._get_config("model_datetime_columns") or None 
            if datetime_columns is not None: 
                datetime_columns = datetime_columns.split(",")
            else: 
                datetime_columns = []

        data_profile_dict = {
            "dataframes" : [data],
            "entry_names" : entry_names, 
            "datetime_columns" : datetime_columns, 
            "index_column" : index_column, 
            "time_index_column" : time_index_column,
        }
        
        return data_profile_dict, None

    def compare_data(self, data, prev_data, **kwargs): 
        # not implemented
        pass 
