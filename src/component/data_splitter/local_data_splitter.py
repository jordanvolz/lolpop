from component.data_splitter.abstract_data_splitter import AbstractDataSplitter
from utils import common_utils as utils
import pandas as pd 

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class LocalDataSplitter(AbstractDataSplitter): 
    __REQUIRED_CONF__ = {
        "config" : ["MODEL_TARGET", "DROP_COLUMNS"]
    }

    def __init__(self, conf, pipeline_conf, runner_conf, **kwargs): 
        super().__init__(conf, pipeline_conf, runner_conf, **kwargs)

    def split_data(self, data, **kwargs):
        #data["AVERAGE_WORD_LENGTH"] = data["AVERAGE_WORD_LENGTH"].astype(float) #doesn't come back from snowflake
        data_out = data.drop(self._get_config("DROP_COLUMNS",[]),axis=1, errors="ignore")
        data_out = self._split_data(
            data_out, 
            self._get_config("MODEL_TARGET"), 
            split_column = self._get_config("SPLIT_COLUMN", None),
            split_classes = self._get_config("SPLIT_CLASSES", {}),  
            split_ratio = self._get_config("SPLIT_RATIO", [0.8, 0.2]), 
            sample_num = self._get_config("SAMPLE_NUM", 100000), 
            use_startified = self._get_config("USE_STRATIFIED", False),
            include_test = self._get_config("INCLUDE_TEST", False),
            )
        for key in data_out.keys():
            self.log("Created %s dataset with %s rows" %(key, data_out.get(key).shape[0]))

        return data_out

    #function to split data. 
    #Supports random splitting, manual splitting, and stratified. 
    #Can also include test set. 
    def _split_data(self, data, target,  split_column=None, split_classes={},  split_ratio=[0.8,0.2], sample_num=100000, use_startified=False, include_test=False): 
        data_out = {}
        test = None 

        #if a split_column is provided, then we assume you wanted to handle everything yourself
        if split_column is not None: 
            train = data[data[split_column] == split_classes["train"]]
            valid = data[data[split_column] == split_classes["valid"]]
            if include_test: 
                test = data[data[split_column] == split_classes["test"]]
            data_out = self._build_split_dfs(train, valid, target, split_column, test)

        else: #random sample
            if use_startified: 
                strat_df = data.groupby(target, group_keys=False).apply(lambda x: x.sample(min(len(x), 2)))
            if data.shape[0] > sample_num: 
                data = data.sample(sample_num)

            train = data.sample(frac=split_ratio[0])
            valid = data.drop(train.index)
            
            if include_test: 
                temp_valid = valid.copy()
                valid = temp_valid.sample(frac=(split_ratio[1]/(split_ratio[1]+split_ratio[2])))
                test = temp_valid.drop(valid.index)
            
            if use_startified: 
                train = train.merge(strat_df, how="outer")
                valid = valid.merge(strat_df, how="outer")
                if include_test:
                    test = test.merge(strat_df, how="outer")
            
            data_out = self._build_split_dfs(train, valid, target, test=test)

        return data_out 

    def _build_split_dfs(self, train, valid, target,  split_column="SPLIT", test=None): 
        data_out = {
            "X_train" : train.drop([target, split_column], axis=1, errors="ignore"), 
            "X_valid" : valid.drop([target, split_column], axis=1, errors="ignore"), 
            "y_train": train[target], 
            "y_valid": valid[target], 
        }
        #include test set if specified
        if test is not None: 
            data_out["X_test"] = test.drop([target, split_column], axis=1, errors="ignore")
            data_out["y_test"] = test[target]

        return data_out

    def _get_train_test_dfs(self, data, combine_xy=True, combine_train_valid=True):
        if combine_train_valid: 
            df_X = pd.concat([data["X_train"],data["X_valid"]])
            df_y = pd.concat([data["y_train"],data["y_valid"]])
        else: 
            df_X = data["X_train"]
            df_y = data["y_train"]

        if combine_xy: 
            train = pd.concat([df_X,df_y],axis=1)
            test = pd.concat([data["X_test"], data["y_test"]], axis=1)
        else: 
            train = (df_X, df_y)
            test = (data["X_test"], data["y_test"])

        return train, test 