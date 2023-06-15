```
class MetaflowPipelineWrapper(BaseWrapper):
     """
     A class to wrap Metaflow scripts for execution and tracking the pipeline's status. 

     Attributes:
         MetaflowPipelineWrapper inherits all attributes from BaseWrapper

     Methods:
         run():
             Starts the Metaflow pipeline script specified in the config file at "metaflow_script".
             Gets the status of pipeline using flow_id and logs the status. 

     """


    def run(self):
        """
        Starts the Metaflow pipeline script specified in the config file at "metaflow_script". 
        Gets the status of pipeline from the "flow_id" specified in the config file.
        Logs the pipeline status.

        Args:
            None.

        Returns:
            None.
        
        Raises:
            None.

        """
        metaflow_path = self._get_config("metaflow_script") 
        result, _ = utils.execute_cmd(["python3", metaflow_path, "run"], self)
        
        #self.log(result)

        # Get the pipeline status and log it
        flow_id = self._get_config("flow_id")
        if flow_id: 
            flow = Flow(flow_id)
            if flow.latest_run.successful:
                status = "successful"
            else: 
                status = "unsuccessful"
            self.log("Metaflow pipline %s completed. Status is %s" %(flow.latest_run.pathspec,status))
```