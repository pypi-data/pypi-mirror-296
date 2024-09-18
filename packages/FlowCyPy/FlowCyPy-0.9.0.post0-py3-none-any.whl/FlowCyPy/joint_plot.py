import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Tuple
from MPSPlots.styles import mps
import pandas as pd

class PeakPlotter:
    def __init__(self, dataframe: pd.DataFrame, peak_properties: pd.DataFrame, style: str = mps):
        """
        Initializes the PeakPlotter with a dataframe containing the signal data
        and peak properties for annotation.

        Args:
            dataframe (pd.DataFrame): Data containing 'Signal' values with proper units in .attrs.
            peak_properties (pd.DataFrame): Data containing peak characteristics (PeakTimes, Widths, LeftIPs, RightIPs).
            style (str): Matplotlib style context for the plot.
        """
        self.dataframe = dataframe
        self.peak_properties = peak_properties
        self.style = style

        with plt.style.context(self.style):
            self._initialize_plot()

    def _initialize_plot(self):
        """Prepare the figure and configure axes."""
        self.figure, self.ax = plt.subplots()
        self._configure_axes()

    def _configure_axes(self):
        """Configure the plot's axes, labels, and units."""
        self.ax.plot(self.dataframe.index, self.dataframe['Signal'], label='Signal')

        self.ax.set_xlabel(f'Time [{self.dataframe.index.values.units}]')
        self.ax.set_ylabel(f'Signal [{self.dataframe.Signal.values.units}]')

    def add_peaks(self, peak_color: str = 'red'):
        """
        Add vertical lines to mark the peak positions on the plot.

        Args:
            peak_color (str): Color of the peak markers. Default is 'red'.
        """
        transform = self.ax.get_xaxis_transform()
        for _, peak in self.peak_properties.iterrows():
            self.ax.vlines(x=peak['PeakTimes'], ymin=0, ymax=1, transform=transform, color=peak_color, label='Peak')

    def add_areas(self, area_color: str = 'red', alpha: float = 0.3):
        """
        Add shaded areas under the peaks based on their widths.

        Args:
            area_color (str): Color of the shaded area. Default is 'red'.
            alpha (float): Transparency of the shaded area. Default is 0.3.
        """
        for _, peak in self.peak_properties.iterrows():
            left_bound = peak['LeftIPs'] - (peak['Widths'] / 2)
            right_bound = peak['RightIPs'] + (peak['Widths'] / 2)

            mask = (self.dataframe.index >= left_bound) & (self.dataframe.index <= right_bound)
            if mask.any():
                self.ax.fill_between(self.dataframe.index, y1=0, y2=self.dataframe['Signal'], where=mask,
                                     color=area_color, alpha=alpha)

    def show(self):
        """Display the final plot with legends."""
        self._deduplicate_legend()
        plt.show()

    def _deduplicate_legend(self):
        """Remove duplicate entries in the plot legend."""
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys())



class JointPlotWithMarginals:
    """
    A class to create a joint plot with multiple datasets, KDE, and scatter plots, along with marginal KDE plots.

    Attributes:
        datasets (List[Tuple[np.ndarray, np.ndarray, str]]): List of datasets in the form (x, y, label).
        figure (sns.JointGrid): The JointGrid object for creating the joint plot.
    """

    def __init__(self, xlabel: str = "X-axis", ylabel: str = "Y-axis", figure_size: Tuple[float, int] = (7, 7), log_plot: bool = False):
        """
        Initializes the JointPlotWithMarginals class.

        Args:
            xlabel (str, optional): Label for the x-axis. Defaults to "X-axis".
            ylabel (str, optional): Label for the y-axis. Defaults to "Y-axis".
            figure_size (Tuple[float, int], optional): Figure size with height and ratio. Defaults to (6, 2).
        """
        self.datasets = []
        self.figure = None
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.figure_size = figure_size
        self.log_plot = log_plot


    def add_dataset(
            self,
            x: np.ndarray,
            y: np.ndarray,
            label: str = '',
            alpha: float = 0.3,
            color: Optional[str] = None) -> None:
        """
        Adds a dataset to the joint plot, with KDE and scatter plots.

        Args:
            x (np.ndarray): Data for the x-axis.
            y (np.ndarray): Data for the y-axis.
            label (str): Label for the dataset.
            alpha (float, optional): Transparency level for the plots. Defaults to 0.3.
            color (str, optional): Color for the dataset. If None, a color will be chosen automatically.

        Raises:
            ValueError: If x and y do not have matching lengths.
        """
        if len(x) != len(y):
            raise ValueError(f"Dataset '{label}' has mismatched x and y lengths.")

        # Add the dataset to the list of datasets
        self.datasets.append([x, y, label, alpha, color])

        # Initialize the JointGrid if it's the first dataset
        if self.figure is None:
            height, ratio = self.figure_size
            g = self.figure = sns.JointGrid(x=x, y=y, height=height, ratio=ratio)
            if self.log_plot:
                ax = g.ax_joint
                ax.set_xscale('log')
                ax.set_yscale('log')
                g.ax_marg_x.set_xscale('log')
                g.ax_marg_y.set_yscale('log')

        # Initialize the JointGrid if it's the first dataset
        if self.figure is None:
            self.figure = sns.JointGrid(x=x, y=y)

        # Use default color if none is provided
        if color is None:
            color = sns.color_palette("husl", len(self.datasets))[len(self.datasets) - 1]

            self.datasets[-1][-1] = color

        # Add KDE and scatter plots
        self._add_kde_plot(x, y, color, label, alpha)
        self._add_scatter_plot(x, y, color, label, alpha)

    def _add_kde_plot(self, data_x: np.ndarray, data_y: np.ndarray, color: str, label: str = '', alpha: float = 0.5) -> None:
        """
        Adds a KDE plot to the joint plot and marginals.

        Args:
            data_x (np.ndarray): Data for the x-axis.
            data_y (np.ndarray): Data for the y-axis.
            color (str): Color for the marginal KDE plots.
            label (str): Label for the dataset.
            alpha (float): Transparency level for the plots.
        """
        # Joint KDE plot
        sns.kdeplot(x=data_x, y=data_y, fill=True, ax=self.figure.ax_joint, color=color, alpha=alpha, label=label, warn_singular=False)

        # Marginal KDE plots
        # sns.histplot(x=data_x, ax=self.figure.ax_marg_x, color=color, fill=True, alpha=alpha)
        # sns.histplot(y=data_y, ax=self.figure.ax_marg_y, color=color, fill=True, alpha=alpha)

        sns.kdeplot(x=data_x, ax=self.figure.ax_marg_x, color=color, fill=True, alpha=alpha)
        sns.kdeplot(y=data_y, ax=self.figure.ax_marg_y, color=color, fill=True, alpha=alpha)

    def _add_scatter_plot(self, data_x: np.ndarray, data_y: np.ndarray, color: str, label: str = '', alpha: float = 0.9, size: int = 20) -> None:
        """
        Adds a scatter plot to the joint plot.

        Args:
            data_x (np.ndarray): Data for the x-axis.
            data_y (np.ndarray): Data for the y-axis.
            color (str): Color of the scatter points.
            label (str): Label for the scatter plot.
            alpha (float): Transparency level for the scatter plot.
            size (int, optional): Size of the scatter points. Defaults to 20.
        """
        sns.scatterplot(x=data_x, y=data_y, color=color, ax=self.figure.ax_joint, label=label, s=size, alpha=alpha)

    def add_legend(self) -> None:
        """
        Adds a legend to the joint plot.
        """
        handles = [
            plt.Line2D([0], [0], color=color, lw=4, label=label)
            for _, _, label, _, color in self.datasets
        ]
        self.figure.ax_joint.legend(handles=handles, loc='upper right')

    def generate(self) -> None:
        """
        Generate the figure.
        """
        if self.figure is None:
            raise RuntimeError("No datasets have been added. Add at least one dataset before calling show_plot().")

        self.figure.ax_joint.set_xlabel(self.xlabel)
        self.figure.ax_joint.set_ylabel(self.ylabel)
        self.add_legend()
        plt.tight_layout()


    def show(self) -> None:
        """
        Displays the final plot.
        """
        if self.figure is None:
            raise RuntimeError("No datasets have been added. Add at least one dataset before calling show_plot().")

        plt.show()
