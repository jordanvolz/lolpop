from lolpop.component.base_component import BaseComponent

class BaseDataSplitter(BaseComponent): 

    def split_data(self, data, *args, **kwargs): 
        pass 

    def get_train_test_dfs(self, data,*args, **kwargs): 
        pass 
