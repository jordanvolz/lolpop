from component.data_transformer.abstract_data_transformer import AbstractDataTransformer
from utils import common_utils as utils
from omegaconf import OmegaConf 

@utils.decorate_all_methods([utils.error_handler,utils.log_execution()])
class dbtDataTransformer(AbstractDataTransformer): 
    #use load_config to allow setting these via env variables
    #__REQUIRED_CONF__ = {
    #    "config" : ["DBT_TARGET", "DBT_PROFILE", "DBT_PROJECT_DIR", "DBT_PROFILES_DIR", "data_loader"]
    #}
    def __init__(self, conf, pipeline_conf, runner_conf, **kwargs): 
        super().__init__(conf, pipeline_conf, runner_conf, **kwargs)

        self.dbt_config = utils.load_config(["DBT_TARGET", "DBT_PROFILE", "DBT_PROJECT_DIR", "DBT_PROFILES_DIR"], self.config)

        data_loader = self._get_config("data_loader")

        #dbt doesn't actually retrieve data, so we have to use another data_transformer class to do that. 
        # we'll read credentials for that in the dbt profile though, so you don't have to additionally include that
        # in your dbt configuration
        #note that we don't use utils.register_class_component here because we need to look up the config externally in the dbt profile.
        # in the future we may clean these different paths up. 
        if data_loader is not None: 
            module = __import__("component")
            cl = getattr(module, data_loader)
            config = get_dw_config_from_profile(self.dbt_config)
            obj = cl(config, self.pipeline_conf, self.runner_conf, **kwargs)
            setattr(self,"data_loader",obj)

    def get_data(self, **kwargs): 
        pass 

    def transform(self, data, **kwargs):
        command = "dbt run --target %s --project-dir %s --profiles-dir %s --profile %s" %(
            self.dbt_config.get("DBT_TARGET"), 
            self.dbt_config.get("DBT_PROJECT_DIR"), 
            self.dbt_config.get("DBT_PROFILES_DIR"),
            self.dbt_config.get("DBT_PROFILE")
        )

        output, exit_code = utils.execute_cmd(command)

        self.log("dbt output: \n%s" %output, "INFO")

        if int(exit_code) == 0: #dbt ran successfully
            table_to_load = self._get_config("table_train")

            if self._get_config("pipeline_type") == "predict": 
                table_to_load = self._get_config("table_eval")

            data = self.data_loader.get_data(table_to_load)

        return data 

def get_dw_config_from_profile(dbt_config): 
    conf = OmegaConf.load("%s/profiles.yml" %dbt_config.get("DBT_PROFILES_DIR")).get(dbt_config.get("DBT_PROFILE")).get("outputs").get(dbt_config.get("DBT_TARGET"))
    config = {x.lower():y for x,y in conf.items() if x.lower() in ["account", "database", "password", "schema", "user", "warehouse"]}

    return config 