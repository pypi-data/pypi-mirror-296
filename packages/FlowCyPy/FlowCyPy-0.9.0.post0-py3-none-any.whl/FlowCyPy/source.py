
from dataclasses import dataclass
from FlowCyPy.units import Quantity, meter, watt, distance, power
from FlowCyPy.utils import PropertiesReport
from tabulate import tabulate
import numpy as np

@dataclass()
class Source(PropertiesReport):
    """
    optical_power : Quantity
        The optical power of the laser (in watts).
    wavelength : Quantity
        The wavelength of the laser (in meters).
    """
    optical_power: power
    wavelength: distance
    numerical_aperture: Quantity
    name: str = 'Laser source'

    def __post_init__(self) -> None:
        """
        Initialize additional parameters after class instantiation by assigning physical units to parameters.
        """
        self._add_units_to_parameters()

        # Calculate Gaussian beam waist at the focus
        self.waist = self.wavelength / (np.pi * self.numerical_aperture)

    def _add_units_to_parameters(self) -> None:
        """Adds physical units to the core parameters of the Source."""
        self.optical_power = Quantity(self.optical_power, watt)
        self.wavelength = Quantity(self.wavelength, meter)
