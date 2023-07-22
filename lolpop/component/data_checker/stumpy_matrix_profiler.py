from lolpop.component.data_checker.base_data_checker import BaseDataChecker
from lolpop.utils import common_utils as utils
import stumpy
import numpy as np 
from matplotlib import pyplot as plt 
from matplotlib.patches import Rectangle

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class StumpyMatrixProfiler(BaseDataChecker):
    __REQUIRED_CONF__ = {
        "config": ["local_dir", "model_target"]
    }


    __DEFAULT_CONF__ = {
        "config": {
            "stumpy_analysis_image_name": "STUMPY_DISCORD_ANALYSIS.PNG",
            "stumpy_window_size": [30],
            "stumpy_num_discords": 3,
            }
    }
    

    def check_data(self, data, *args, **kwargs):
        """
        Method for detecting anomalies/novelties in time series data using STUMPY matrix profiling algorithm and plotting the results.

        This method uses STUMPY algorithm for discord discovery in time series data. The algorithm involves sliding a window across
        the time series data and calculating the matrix profile (a distance profile between subsequences). The subsequence corresponding
        to each discovered anomaly/novelty in the time series data will have a distance profile value greater than other subsequence's
        corresponding to a similar or identical anomaly/novelty.

        Parameters:
        data (pandas.DataFrame): Input time series data.
        args (*args): Optional positional arguments to the method.
        kwargs (**kwargs): Optional keyword arguments to the method.

        Returns:
        tuple(None, str, str): Tuple of Nones and the path of the output image, and a string 'ERROR', 'WARN', 'PASS' based on the validity of the input data.
        """
        model_target = self._get_config("MODEL_TARGET")

        windows = self._get_config("stumpy_window_size")
        num_discords = self._get_config("stumpy_num_discords")

        #set up plot
        fig, axs = plt.subplots(len(windows)+1, sharex=True, gridspec_kw={'hspace': 0})
        plt.suptitle('Discord (Anomaly/Novelty) Discovery', fontsize='30')
        axs[0].plot(data[model_target].values)
        axs[0].set_ylabel('TS', fontsize='10')
        box_height = int(data[model_target].max())

        j=1
        for m in windows: 
            #calculate matrix profile
            mp = stumpy.stump(data[model_target], m)
            discords = []
            #find top n discords. These are the most likely anomalies in the data.
            for i in range(1, num_discords+1):
                discord_idx = np.argsort(mp[:, 0])[-i]
                nearest_neighbor_distance = mp[discord_idx, 0]
                discords.append(discord_idx)
                self.log("Found possible anomaly at index %s, which is %s units from its nearest neighbor" %(discord_idx, nearest_neighbor_distance))    
            #plot the matrix profile
            self.__plot_mp(axs, m, box_height, mp, discords, j)
            j=j+1

        #save plot
        file_path = "%s/%s" %(self._get_config("local_dir"), self._get_config("stumpy_analysis_image_name"))
        plt.savefig(file_path)

        return None, file_path, "PASS"

    def __plot_mp(self, axs, m, h, mp, discords, i): 
        """
        Private method for plotting the STUMPY matrix and marking the discovered anomalies/novelties.

        This method plots the STUMPY matrix for the given subsequence length and marks the discovered anomalies/novelties in the time series data.

        Parameters:
        axs (list of matplotlib axes): List of matplotlib axes to plot the matrix.
        m  (int): Subsequence length for STUMPY matrix.
        h (int): Height of box for marking the anomalies/novelties.
        mp (numpy array): STUMPY matrix to be plotted.
        discords (list of int): Indices of the discovered anomalies/novelties in the time series data.
        i (int): Index in axs list where the plot will be made.

        Returns:
        None
        """
        axs[i].set_ylabel('MP (m=%s)' %m, fontsize='10')
        axs[i].set_xlabel('Time', fontsize='10')
        axs[i].plot(mp[:, 0])
         
        for discord_idx in discords: 
            if i == 1:  # only add rectangles for the first window, otherwise it's going to get cluttered.
                rect = Rectangle((discord_idx, 0), m, h, facecolor='lightgrey')
                axs[0].add_patch(rect)
            axs[i].axvline(x=discord_idx, linestyle="dashed")
