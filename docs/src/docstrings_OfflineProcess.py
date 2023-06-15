```
class OfflineProcess(BaseProcess):
  """
  A class used for offline data processing.

  Attributes:
    __REQUIRED_CONF__ (dict): A dictionary containing required configuration components for the class.
        components (list): a list of the components required by this class.
        config (list): a list of the configuration required for this class.

  Methods:
    transform_data(source_data_name):
      Transforms source data by calling data_transformer class method.

      Args:
        source_data_name (str): A string containing the name of source data.

      Returns:
        data_out: The transformed data
      
    track_data(data, id):
      Tracks the data by creating a dataset version and registering version control metadata.

      Args:
        data: Data to be tracked.
        id: The id of the dataset version.

      Returns:
        dataset_version: The dataset version of the registered version control metadata.

    profile_data(data, dataset_version):
      Profiles the data by logging the data profile to metadata tracker.

      Args:
        data: Data to be profiled.
        dataset_version: The dataset version of the registered version control metadata.

      Returns:
        None

    check_data(data, dataset_version):
      Checks the data by logging a data report to the metadata tracker and sending a notification if `checks_status` is `ERROR` or `WARN`.

      Args:
        data: Data to be checked.
        dataset_version: The dataset version of the registered version control metadata.

      Returns:
        None

    compare_data(data, dataset_version):
      Compares a dataset version with the previous version and logs a comparison report to metadata tracker.

      Args:
        data: Data to be compared.
        dataset_version: The dataset version of the registered version control metadata.

      Returns:
        None
  """
  __REQUIRED_CONF__ = {
    "components": ["data_transformer", "metadata_tracker", "resource_version_control", "data_profiler", "data_checker"], 
    "config": []
  }

  def transform_data(self, source_data_name): 
    """
    Transforms source data by calling data_transformer class method.

    Args:
      source_data_name (str): A string containing the name of source data.

    Returns:
      data_out: The transformed data.
    """
    ##get source data
    #data = self.data_connector.get_data(source_data_name)

    #transform data
    data_out = self.data_transformer.transform(source_data_name)

    return data_out

  def track_data(self, data, id): 
    """
    Tracks the data by creating a dataset version and registering version control metadata.

    Args:
      data: Data to be tracked.
      id: The id of the dataset version.

    Returns:
      dataset_version: The dataset version of the registered version control metadata.
    """
    #create dataset version 
    dataset_version = self.metadata_tracker.create_resource(id, type="dataset_version")
    self.datasets_used.append(dataset_version)
    
    #version data
    vc_info = self.resource_version_control.version_data(dataset_version, data)

    #register version control metadata w/ metadata tracker
    self.metadata_tracker.register_vc_resource(dataset_version, vc_info, file_type="csv")
        
    return dataset_version
      
  def profile_data(self, data, dataset_version): 
    """
    Profiles the data by logging the data profile to metadata tracker.

    Args:
      data: Data to be profiled.
      dataset_version: The dataset version of the registered version control metadata.

    Returns:
      None
    """
    #profile data
    data_profile, file_path = self.data_profiler.profile_data(data)

    #log profile to metadata tracker
    self.metadata_tracker.log_data_profile(
        dataset_version, 
        file_path=file_path, 
        profile=data_profile, 
        profiler_class=type(self.data_profiler).__name__
        )

  def check_data(self, data, dataset_version): 
    """
    Checks the data by logging a data report to the metadata tracker and sending a notification if `checks_status` is `ERROR` or `WARN`.

    Args:
      data: Data to be checked.
      dataset_version: The dataset version of the registered version control metadata.

    Returns:
      None
    """
    #run data checks
    data_report, file_path, checks_status = self.data_checker.check_data(data)

    #log data report to metadata tracker
    self.metadata_tracker.log_checks(
        dataset_version,
        file_path = file_path, 
        report = data_report, 
        checker_class = type(self.data_checker).__name__, 
        type = "data"
        )

    if checks_status == "ERROR" or checks_status == "WARN": 
        url = self.metadata_tracker.url
        self.notify("Issues found with data checks. Visit %s for more information." %url, checks_status)
        
  def compare_data(self, data, dataset_version):
    """
    Compares a dataset version with the previous version and logs a comparison report to metadata tracker.

    Args:
      data: Data to be compared.
      dataset_version: The dataset version of the registered version control metadata.

    Returns:
      None
    """
    #get previous dataset version & dataframe 
    prev_dataset_version = self.metadata_tracker.get_prev_resource_version(dataset_version)

    if prev_dataset_version is not None: 
        vc_info = self.metadata_tracker.get_vc_info(prev_dataset_version)
        prev_data = self.resource_version_control.get_data(prev_dataset_version, vc_info)

        #compare current dataset version with previous dataset version
        comparison_report, file_path = self.data_profiler.compare_data(data, prev_data)

        self.metadata_tracker.log_data_comparison(
            dataset_version,
            file_path = file_path, 
            report = comparison_report, 
            profiler_class = type(self.data_profiler).__name__
            )
    else: 
        self.log("No previous dataset version found for dataset: %s" %(self.metadata_tracker.get_resource_id(dataset_version)))
```