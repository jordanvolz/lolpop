from lolpop.component.data_checker.base_data_checker import BaseDataChecker
from lolpop.utils import common_utils as utils
import stumpy
import numpy as np 
from matplotlib import pyplot as plt 
from matplotlib.patches import Rectangle

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class StumpyMatrixProfiler(BaseDataChecker):

    __REQUIRED_CONF__ = {
        "config": ["local_dir"]
    }

    def check_data(self, data, *args, **kwargs):
        """Generates a data check report using Deepchecks.

        Args:
            data (pd.DataFrame): A dataframe of the data to check

        Returns:
            data_report (object): Python object of the data report.
            file_path (string):  Path to the exported report. 
            checks_status (string): Status of the checks ("PASS"/"WARN"/"ERROR", etc.)
        """
        model_target = self._get_config("MODEL_TARGET")

        windows = self._get_config("stumpy_window_size", [30])
        num_discords = self._get_config("stumpy_num_discords", 3)

        #set up plot
        fig, axs = plt.subplots(len(windows)+1, sharex=True, gridspec_kw={'hspace': 0})
        plt.suptitle('Discord (Anomaly/Novelty) Discovery', fontsize='30')
        axs[0].plot(data[model_target].values)
        axs[0].set_ylabel('TS', fontsize='10')
        box_height = int(data[model_target].max())

        j=1
        for m in windows: 
            mp = stumpy.stump(data[model_target], m)
            discords = []
            for i in range(1, num_discords+1):
                discord_idx = np.argsort(mp[:, 0])[-i]
                nearest_neighbor_distance = mp[discord_idx, 0]
                discords.append(discord_idx)
                self.log("Found possible anomaly at index %s, which is %s units from its nearest neighbor" %(discord_idx, nearest_neighbor_distance))    
            self._plot_mp(axs, m, box_height, mp, discords, j)
            j=j+1


        file_path = "%s/STUMP_DISCORD_ANALSIS.PNG" % self._get_config("local_dir")
        plt.savefig(file_path)

        return None, file_path, "PASS"

    def _plot_mp(self, axs, m, h, mp, discords, i): 
        print("i:" + str(i))
        axs[i].set_ylabel('MP (m=%s)' %m, fontsize='10')
        axs[i].set_xlabel('Time', fontsize='10')
        axs[i].plot(mp[:, 0])
         
        for discord_idx in discords: 
            if i == 1:  # only add rectangles for the first window, otherwise it's going to get cluttered.
                rect = Rectangle((discord_idx, 0), m, h, facecolor='lightgrey')
                axs[0].add_patch(rect)
            axs[i].axvline(x=discord_idx, linestyle="dashed")
