from lolpop.pipeline.wrapper.base_wrapper import BaseWrapper
from lolpop.utils import common_utils as utils

from metaflow import Flow

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class MetaflowPipelineWrapper(BaseWrapper):

    def run(self):
        metaflow_path = self._get_config("metaflow_script") 
        result, _ = utils.execute_cmd(["python3", metaflow_path, "run"], self)
        print(result)

        flow_id = self._get_config("flow_id")
        if flow_id: 
            flow = Flow(flow_id)
            if flow.latest_run.successful:
                status = "successful"
            else: 
                status = "unsuccessful"
            self.log("Metaflow pipline %s completed. Status is %s" %(flow.latest_run.pathspec,status))
        
