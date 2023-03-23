from lolpop.component.data_transformer.base_data_transformer import BaseDataTransformer
from lolpop.utils import common_utils as utils
from omegaconf import OmegaConf 

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class dbtDataTransformer(BaseDataTransformer): 
    
    #use load_config to allow setting "DBT_TARGET", "DBT_PROFILE", "DBT_PROJECT_DIR", "DBT_PROFILES_DIR",  via env variables
    __REQUIRED_CONF__ = {
        "config" : ["data_loader"]
    }

    def __init__(self, conf, pipeline_conf, runner_conf, components={}, *args, **kwargs): 
        super().__init__(conf, pipeline_conf, runner_conf, components=components, *args, **kwargs)

        self.dbt_config = utils.load_config(["DBT_TARGET", "DBT_PROFILE", "DBT_PROJECT_DIR", "DBT_PROFILES_DIR"], self.config)

        data_loader = self._get_config("data_loader")

        #dbt doesn't actually retrieve data, so we have to use another data_transformer class to do that. 
        # we'll read credentials for that in the dbt profile though, so you don't have to additionally include that
        # in your dbt configuration
        if data_loader is not None: 
            config = get_dw_config_from_profile(self.dbt_config)
            obj = utils.register_component_class(self, config, "data_loader", data_loader, self.pipeline_conf, self.runner_conf,
                                           parent_process=self.parent_process, problem_type=self.problem_type, dependent_components=components)

    def get_data(self, source_table_name, *args, **kwargs): 
        """Gets Data. Uses the specified data_loader to get the requested table.

        Args:
            source_table_name (String): Name of table to retrieve

        Returns:
            pd.DataFrame: The data
        """
        return self.data_loader.get_data(source_table_name, *args, **kwargs)

    def transform(self, data, source_table_name, *args, **kwargs):
        """Runs dbt workflow, specifid by dbt configuration provided. 

        Args:
            data (None): Unused
            source_table_name (String): Name of the table to load and return. This should be a
              table created in the dbt workflow.

        Returns:
            pd.DataFrame: the transformed data
        """
        command = "dbt run --target %s --project-dir %s --profiles-dir %s --profile %s" %(
            self.dbt_config.get("DBT_TARGET"), 
            self.dbt_config.get("DBT_PROJECT_DIR"), 
            self.dbt_config.get("DBT_PROFILES_DIR"),
            self.dbt_config.get("DBT_PROFILE")
        )

        output, exit_code = utils.execute_cmd(command)

        self.log("dbt output: \n%s" %output, "INFO")

        if int(exit_code) == 0: #dbt ran successfully
            data = self.data_loader.get_data(source_table_name)

        return data 

def get_dw_config_from_profile(dbt_config):
    """Retrieves DW configurtion from dbt profile. 

    Args:
        dbt_config (dict): dictionary containing the dbt configuraiton

    Returns:
        dict: The DW configuration
    """
    conf = OmegaConf.load("%s/profiles.yml" %dbt_config.get("DBT_PROFILES_DIR")).get(dbt_config.get("DBT_PROFILE")).get("outputs").get(dbt_config.get("DBT_TARGET"))
    config = {x.lower():y for x,y in conf.items() if x.lower() in ["account", "database", "password", "schema", "user", "warehouse"]}
    config = OmegaConf.create({"components": {}, "data_loader": {"config": config}})
    
    return config 