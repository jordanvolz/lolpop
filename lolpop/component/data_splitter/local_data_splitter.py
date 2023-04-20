from lolpop.component.data_splitter.base_data_splitter import BaseDataSplitter
from lolpop.utils import common_utils as utils
import pandas as pd 

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class LocalDataSplitter(BaseDataSplitter): 
    
    __REQUIRED_CONF__ = {
        "config" : ["MODEL_TARGET", "DROP_COLUMNS"]
    }

    def split_data(self, data, **kwargs):
        """_summary_

        Args:
            data (pd.DataFrame): DataFrame to split

        Returns:
            data_out (dict(pd.DataFrame)): A dictionary of dataframes. Depending on 
                the provided configuration it can contain the following: 
                    X_train = Features of the training dataset  
                    y_train = Labels of the training dataset 
                    X_valid = Features of the validation dataset
                    y_valid = Labels of the validation dataset
                    X_test = Features of the test/holdout dataset
                    y_test = Labels of the validation dataset

        """
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

    def _split_data(self, data, target,  split_column=None, split_classes={},  split_ratio=[0.8,0.2], sample_num=100000, use_startified=False, include_test=False): 
        """ Function to split data. 
            Supports random splitting, manual splitting, and stratified. 
            Can also include test set. 

        Args:
            data (pd.DataFrame): Dataframe to split
            target (string): The model target, or label 
            split_column (string, optional): The column to use for a manual split. Defaults to None.
            split_classes (dict(string), optional): A dictionary that maps column values to split datasets. I.E.
              Something like {"train" : "train", "valid" : "valid", "test" : "test"}. This allows you to use arbitrary 
              values in your manual split. This is required if split_column is provided. 
            split_ratio (list(float), optional): The percentage of data to put in each split dataset. This should 
             contain either 2 or 3 floats, representing train, valid, test (optional) datasets, respectively. This
              should also add up to 1!  Not used if a manual split is specified. Defaults to [0.8,0.2].
            sample_num (int, optional): The number of rows to include in your dataset. This is the total 
              number across train, valid, and test sets. Defaults to 100000.
            use_startified (bool, optional): Whether or not to used stratified sampling. When doing classifications problems, 
              some frameworks will error out when classes with no cardinality do not appear in one of the datasets. Statified sampling
              ensures that at least one member of each class will appear in each dataset. Defaults to False.
            include_test (bool, optional): If a holdout dataset should be created. Defaults to False.

        Returns:
            data_out (dict(pd.DataFrame)): A dictionary of dataframes. Depending on 
                the provided configuration it can contain the following: 
                    X_train = Features of the training dataset  
                    y_train = Labels of the training dataset 
                    X_valid = Features of the validation dataset
                    y_valid = Labels of the validation dataset
                    X_test = Features of the test/holdout dataset
                    y_test = Labels of the validation dataset
        """
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
        """Builds the dictionary of split datasets from the individual dataframes. 

        Args:
            train (pd.Dataframe): training dataframe
            valid (pd.DataFrame): validation dataframe
            target (string): the model target, or label
            split_column (str, optional): the column specifying the manual split, if used.  Defaults to "SPLIT".
            test (pd.DataFrame, optional): test dataframe. Defaults to None.

        Returns:
            data_out (dict(pd.DataFrame)): A dictionary of dataframes. Depending on 
                the provided configuration it can contain the following: 
                    X_train = Features of the training dataset  
                    y_train = Labels of the training dataset 
                    X_valid = Features of the validation dataset
                    y_valid = Labels of the validation dataset
                    X_test = Features of the test/holdout dataset
                    y_test = Labels of the validation dataset
        """
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

    def get_train_test_dfs(self, data, combine_xy=True, combine_train_valid=True):
        """Given the dictionary of split data sets, this produces combined training and test dataframes. 

        Args:
            data (dict(pd.Dataframes)): A dictionary of dataframes. Should be the output of split_data
            combine_xy (bool, optional): Whether to combine features with the model label. Defaults to True.
            combine_train_valid (bool, optional): Whether to combine training and validation datasets. Defaults to True.

        Returns:
            (train, test): a duple of dataframes 
        """
        if combine_train_valid: 
            df_X = pd.concat([data["X_train"],data["X_valid"]], ignore_index=True)
            df_y = pd.concat([data["y_train"],data["y_valid"]], ignore_index=True)
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