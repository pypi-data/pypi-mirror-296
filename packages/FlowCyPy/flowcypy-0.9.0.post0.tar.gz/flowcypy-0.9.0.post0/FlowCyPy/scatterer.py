from typing import List, Optional
import matplotlib.pyplot as plt
from MPSPlots.styles import mps
from dataclasses import dataclass
import numpy as np
import pandas as pd
from FlowCyPy.units import refractive_index_unit
from FlowCyPy.flow_cell import FlowCell
from FlowCyPy.population import Population
from FlowCyPy.joint_plot import JointPlotWithMarginals
from FlowCyPy.utils import PropertiesReport

@dataclass
class Scatterer(PropertiesReport):
    """
    Defines and manages the size and refractive index distributions of scatterers (particles)
    passing through a flow cytometer. This class generates random scatterer sizes and refractive
    indices based on a list of provided distributions (e.g., Normal, LogNormal, Uniform, etc.).

    Attributes
    ----------
    flow : object
        The flow setup used to determine the number of particles (n_events).
    refractive_index : Union[float, List[distribution.Base]]
        A single refractive index or a list of refractive index distributions.
    size : Union[float, List[distribution.Base]]
        A single particle size or a list of size distributions.
    coupling_factor : str, optional
        The type of coupling factor to use. Options are 'rayleigh' or 'uniform'. Default is 'rayleigh'.
    """

    flow_cell: FlowCell  # Flow object defining flow properties
    populations: List[Population]
    coupling_factor: Optional[str] = 'mie'  # Coupling factor type ('rayleigh', 'uniform')
    medium_refractive_index: float = 1.0 * refractive_index_unit # Refractive index or refractive index distributions

    def __post_init__(self) -> None:
        """Initializes particle size, refractive index, and medium refractive index distributions."""

        for population in self.populations:
            population.initialize(flow_cell=self.flow_cell)

        self.size_list = np.concatenate(
            [p.size_list for p in self.populations]
        )

        self.refractive_index_list = np.concatenate(
            [p.refractive_index_list for p in self.populations]
        )

        self.dataframe = pd.concat(
            [p.dataframe for p in self.populations],
            axis=0,
            keys=[p.name for p in self.populations],
        )

        self.dataframe.index.names = ['Population', 'Index']

    def plot(self, show: bool = True, figure_size: tuple = (5, 5), log_plot: bool = False) -> None:
        """
        Visualizes the joint distribution of scatterer sizes and refractive indices using a Seaborn `jointplot`.

        This method plots the relationship between the scatterer sizes and refractive indices, including both
        their marginal distributions (as Kernel Density Estimates, KDEs) and a scatter plot overlay.

        The `jointplot` displays:
            - **Marginal KDE plots** for scatterer sizes (on the x-axis) and refractive indices (on the y-axis).
            - **Scatter plot** showing the relationship between the sizes and refractive indices.
            - **Joint KDE plot** to highlight the density of points in the scatter plot.

        The marginal and joint KDEs are filled to provide better visualization of density.
        """
        # Reset the index if necessary (to handle MultiIndex)
        df_reset = self.dataframe.reset_index()

        # Extract the units from the pint-pandas columns
        x_unit = df_reset['Size'].pint.units

        import seaborn as sns
        with plt.style.context(mps):
            g = sns.jointplot(
                data=df_reset,
                x='Size',
                y='RefractiveIndex',
                hue='Population',
                kind='kde',
                alpha=0.8,
                fill=True,
                joint_kws={'alpha': 0.7}
            )

            sns.scatterplot(
                data=df_reset,
                x='Size',
                y='RefractiveIndex',
                hue='Population',
                ax=g.ax_joint,
                alpha=0.6,
                zorder=1
            )

            # Set the x and y labels with units
            g.ax_joint.set_xlabel(f"Size [{x_unit}]")

            plt.tight_layout()

            if log_plot:
                ax = g.ax_joint
                ax.set_xscale('log')
                ax.set_yscale('log')
                g.ax_marg_x.set_xscale('log')
                g.ax_marg_y.set_yscale('log')


            if show:
                plt.show()

    def print_properties(self) -> None:
        return super(Scatterer, self).print_properties(
            ['coupling_factor', 'medium_refractive_index']
        )
