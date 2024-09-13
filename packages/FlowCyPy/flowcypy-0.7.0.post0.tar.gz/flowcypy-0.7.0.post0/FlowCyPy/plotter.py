from dataclasses import dataclass
from typing import Optional
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from MPSPlots.styles import mps
from FlowCyPy.dataset import DataSet
from FlowCyPy.joint_plot import JointPlotWithMarginals

@dataclass
class Plotter:
    """
    A class to plot a 2D density plot of scattering intensities detected by two detectors.

    This class takes two detectors' scattering intensities and plots a 2D hexbin density plot,
    with a horizontal colorbar and custom axis labels positioned on the top and right.

    Attributes
    ----------
    dataset_0 : object
        Scattering data from detector 0, expected to have 'time' and 'height' attributes.
    dataset_1 : object
        Scattering data from detector 1, expected to have 'time' and 'height' attributes.
    gridsize : Optional[int], optional
        The number of hexagonal bins for the 2D histogram (default is None).
    bins : Optional[int], optional
        Number of bins for the marginal histograms (default is 30).
    """

    dataset_0: DataSet  # Data from detector 0
    dataset_1: DataSet  # Data from detector 1
    gridsize: Optional[int] = None  # Default gridsize for hexbin
    bins: Optional[int] = 30  # Default number of bins for marginal histograms

    def plot(self) -> None:
        """
        Plots the 2D density plot of the scattering intensities from the two detectors.

        The plot includes:
        - A 2D hexbin density plot.
        - X-axis label positioned on top and y-axis label positioned on the right.
        - A horizontal colorbar at the bottom indicating the density.
        """
        # Set seaborn style for better aesthetics

        with plt.style.context(mps):

            join_plot = JointPlotWithMarginals(
                xlabel=f'Detector {self.dataset_0.detector.name} Scattering Intensity [{self.dataset_0.height.units}]',
                ylabel=f'Detector {self.dataset_1.detector.name} Scattering dsdasdsa Intensity [{self.dataset_1.height.units}]'
            )

            join_plot.add_dataset(
                x=self.dataset_0.height.magnitude,
                y=self.dataset_1.height.magnitude,
                alpha=0.9,
            )

            join_plot.show_plot()
