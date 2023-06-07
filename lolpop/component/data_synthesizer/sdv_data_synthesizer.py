from lolpop.component.data_synthesizer.base_data_synthesizer import BaseDataSynthesizer
from lolpop.utils import common_utils as utils
import pandas as pd 
from sdv.metadata import SingleTableMetadata

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class SDVDataSynthesizer(BaseDataSynthesizer):

    __DEFAULT_CONF__ = {
        "config": {
            "synthesizer" : "SingleTablePreset"
        }
    }

    def load_data(self, source_file_path, file_type="csv", *args, **kwargs):
        """Loads data for data synthesizer. 

        Args:
            source_file_path (string): path to the file (local)
            file_type (str, optional): Type of file. Defaults to "csv".

        Returns:
            pd.DataFrame: dataframe of the data 
            metadata: sdv metadata of the dataframe
        """
        df = utils.create_df_from_file(source_file_path, **kwargs)
        
        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=df)

        return df, metadata 

    def model_data(self, data, metadata, synthesizer_str=None, *args, **kwargs):
        """Creates a synthesizer of the given data. 

        Args:
            data (pd.Dataframe): Data to synthesize. 
            metadata (dict): Metadata of the data. Should be ouput from load_data. 

        Returns:
            _type_: _description_
        """
        synthesizer = None 

        if synthesizer_str is None: 
            synthesizer_str = self._get_config("synthesizer")
        synthesizer_cl = self._get_synthesizer_class(synthesizer_str)

        if synthesizer_cl is not None: 
            if synthesizer_str == "SingleTablePreset": 
                kwargs.update({"name": "FAST_ML"}) #required or SingleTablePreset failes
            synthesizer = synthesizer_cl(metadata, **kwargs)
            synthesizer.fit(data)

        return synthesizer

    def sample_data(self, synthesizer, num_rows, *args, **kwargs):
        """sample data from the given synthesizer

        Args:
            synthesizer (Object): The synthesizer. Should be the output from model_data
            num_rows (int): The number of rows to generate

        Returns:
            pd.DataFrame: A dataframe of synthesized data
        """
        data = synthesizer.sample(num_rows=num_rows)

        return data

    def evaluate_data(self, real_data, synthetic_data, metadata, synthesizer_str, *args, **kwargs):
        """Evaluates the synthetic data

        Args:
            real_data (pd.Dataframe): The real data. 
            synthetic_data (pd.Dataframe): The fake data. 
            metadata (dict): Data's metadata. 

        Returns:
            quality_report: report on the quality of the fake data
            diagnostic_report: diagnostic results about the fake data
        """
        if synthesizer_str is None: 
            synthesizer_str = self._get_config("synthesizer")

        evaluator_cl = self._get_evaluator_class(synthesizer_str)
        quality_report = evaluator_cl(real_data = real_data, synthetic_data=synthetic_data, metadata=metadata)
        
        diagnostic_cl = self._get_diagnostic_class(synthesizer_str)
        diagnostic_report = diagnostic_cl(
            real_data=real_data, synthetic_data=synthetic_data, metadata=metadata)
        
        #can also print some charts via sdv.evaluation.single_table.get_column_lot/get_column_pair_plot

        return quality_report, diagnostic_report

    def _get_synthesizer_class(self, synthesizer): 
        cl = None
        if synthesizer == "SingleTablePreset":
            cl = utils.load_class(synthesizer, "lite", "sdv")
        elif synthesizer in ["CTGANSynthesizer", "CopulaGANSynthesizer", "GaussianCopulaSynthesizer", "TVAESynthesizer"]:
            cl = utils.load_class(synthesizer, "single_table", "sdv")
        elif synthesizer == "HMASynthesizer": 
            cl = utils.load_class(synthesizer, "multi_table", "sdv")
        elif synthesizer == "PARSynthesizer": 
            cl = utils.load_class(synthesizer, "sequential", "sdv")
        else: 
            msg = "Unsupported synthesizer: %s" % synthesizer
            self.log(msg, level="ERROR")
            raise Exception(msg)
    
        return cl 

    def _get_evaluator_class(self, synthesizer):
        cl = None
        if synthesizer in ["SingleTablePreset", "CTGANSynthesizer", "CopulaGANSynthesizer", "GaussianCopulaSynthesizer", "TVAESynthesizer"]:
            cl = utils.load_class("evaluate_quality",
                                  "single_table", "sdv.evaluation")
        elif synthesizer == "HMASynthesizer":
            cl = utils.load_class("evaluate_quality",
                                  "multi_table", "sdv.evaluation")
        elif synthesizer == "PARSynthesizer":
            cl = utils.load_class("evaluate_quality",
                                  "sequential", "sdv.evaluation")
        else:
            msg = "Unsupported synthesizer: %s" % synthesizer
            self.log(msg, level="ERROR")
            raise Exception(msg)
        
        return cl 

    def _get_diagnostic_class(self, synthesizer):
        cl = None
        if synthesizer in ["SingleTablePreset", "CTGANSynthesizer", "CopulaGANSynthesizer", "GaussianCopulaSynthesizer", "TVAESynthesizer"]:
            cl = utils.load_class("run_diagnostic", "single_table", "sdv.evaluation")
        elif synthesizer == "HMASynthesizer":
            cl = utils.load_class("evaluate_quality",
                                  "multi_table", "sdv.evaluation")
        elif synthesizer == "PARSynthesizer":
            cl = utils.load_class("evaluate_quality",
                                  "sequential", "sdv.evaluation")
        else:
            msg = "Unsupported synthesizer: %s" % synthesizer
            self.log(msg, level="ERROR")
            raise Exception(msg)

        return cl 