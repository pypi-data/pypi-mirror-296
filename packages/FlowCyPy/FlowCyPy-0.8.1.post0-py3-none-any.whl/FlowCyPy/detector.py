import numpy as np
from typing import Optional, Union, List
import matplotlib.pyplot as plt
from tabulate import tabulate
from FlowCyPy import ureg
from FlowCyPy.utils import array_to_compact
from FlowCyPy.units import Quantity, hertz, volt, watt, degree
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from dataclasses import field
from MPSPlots.styles import mps
import pandas as pd
import pint_pandas


config_dict = dict(
    arbitrary_types_allowed=True,
    kw_only=True,
    slots=True,
    extra='forbid'
)


@dataclass(config=config_dict)
class Detector:
    """
    Represents a detector in a flow cytometer responsible for capturing and processing signals.
    """

    name: str
    sampling_freq: Quantity
    phi_angle: Quantity
    NA: float

    gamma_angle: Optional[Quantity] = Quantity(0, degree)
    sampling: Optional[int] = 100
    responsitivity: Optional[Quantity] = Quantity(1, volt / watt)
    noise_level: Optional[Quantity] = Quantity(0.0, volt)
    baseline_shift: Optional[Quantity] = Quantity(0.0, volt)
    saturation_level: Optional[Quantity] = Quantity(np.inf, volt)
    n_bins: Optional[Union[int, str]] = '12bit'

    # Non-init fields for signal processing
    signal: np.ndarray = field(init=False)
    raw_signal: np.ndarray = field(init=False)
    time: np.ndarray = field(init=False)

    @field_validator('sampling_freq')
    def check_sampling_freq(cls, value):
        """Ensure the sampling frequency is in hertz."""
        if not value.check('Hz'):
            raise ValueError(f"sampling_freq must be in hertz, but got {value.units}")
        return value

    @field_validator('phi_angle', 'gamma_angle')
    def check_angle(cls, value):
        """Ensure angles are in degrees."""
        if not value.check('degree'):
            raise ValueError(f"Angle must be in degrees, but got {value.units}")
        return value

    @field_validator('responsitivity')
    def check_responsitivity(cls, value):
        """Ensure responsitivity is in volts per watt."""
        if not value.check('V / W'):
            raise ValueError(f"Responsitivity must be in volts per watt, but got {value.units}")
        return value

    @field_validator('noise_level', 'baseline_shift', 'saturation_level')
    def check_voltage(cls, value):
        """Ensure the voltage-related attributes are in volts."""
        if not value.check('volt'):
            raise ValueError(f"Voltage-related attributes must be in volts, but got {value.units}")
        return value

    def __post_init__(self) -> None:
        """Initialize units and process the n_bins parameter."""
        self._process_n_bins()
        self._add_units()

    def _add_units(self) -> None:
        """Assign physical units to detector attributes."""
        self.sampling_freq = Quantity(self.sampling_freq, hertz)
        self.responsitivity = Quantity(self.responsitivity, volt / watt)
        self.noise_level = Quantity(self.noise_level, volt)
        self.baseline_shift = Quantity(self.baseline_shift, volt)
        self.saturation_level = Quantity(self.saturation_level, volt)
        self.phi_angle = Quantity(self.phi_angle, degree)
        self.gamma_angle = Quantity(self.gamma_angle, degree)
        self.NA = Quantity(self.NA, 'dimensionless')

    def _process_n_bins(self) -> None:
        """Processes the n_bins attribute, converting bit-depth strings to integer bin count."""
        if isinstance(self.n_bins, str):
            try:
                bit_depth = int(self.n_bins.rstrip('bit'))
                self.n_bins = 2 ** bit_depth
            except (ValueError, TypeError):
                raise ValueError(f"Invalid n_bins value: '{self.n_bins}'. Expected integer or a string like '12bit'.")
        elif not isinstance(self.n_bins, int):
            self.n_bins = 100  # Default to 100 bins if not provided

    def init_raw_signal(self, total_time: float) -> None:
        """Initializes the raw signal and time arrays for a given total time."""
        time_points = int(self.sampling_freq * total_time)
        self.time = array_to_compact(np.linspace(0, total_time, time_points))
        self.dt = self.time[1] - self.time[0]
        self.raw_signal = np.zeros(time_points) * ureg.volt

    def capture_signal(self) -> None:
        """Processes raw signal by applying noise, baseline shifts, and saturation, then discretizes it."""
        self.signal = array_to_compact(self.raw_signal.copy())
        self._apply_baseline_and_noise()
        self._apply_saturation()
        self._discretize_signal()
        self._create_dataframe()

    def _apply_baseline_and_noise(self) -> None:
        """Applies baseline shift and noise to the signal."""
        baseline = self.baseline_shift * np.sin(0.5 * np.pi * self.time.magnitude)
        noise = self.noise_level * np.random.normal(size=len(self.time))
        self.signal += baseline + noise

    def _apply_saturation(self) -> None:
        """Clips the signal to the saturation level."""
        self.signal = np.clip(self.signal, 0, self.saturation_level)

    def _discretize_signal(self) -> None:
        """Discretizes the signal into the specified number of bins."""
        if self.n_bins is not None:
            bins = np.linspace(0, self.saturation_level.magnitude, self.n_bins)
            digitized = np.digitize(self.signal.magnitude, bins) - 1
            self.signal = bins[digitized] * volt

    def _create_dataframe(self) -> None:
        """Creates a pandas DataFrame with Time and Signal as PintArrays."""
        self.dataframe = pd.DataFrame({
            'Signal': pint_pandas.PintArray(self.signal, dtype=self.signal.units),
            'Time': pint_pandas.PintArray(self.time, dtype=self.time.units)
        })
        self.dataframe.set_index('Time', inplace=True)

    def plot(self, show: bool = True, figure_size: tuple = None, color: str = 'C0') -> None:
        """Plots the processed signal."""
        with plt.style.context(mps):
            fig, ax = plt.subplots(figsize=figure_size)
            ax.plot(self.time, self.signal, color=color, label=f'{self.name} Signal')
            ax.set(title=f'Detector: {self.name}', xlabel=f'Time [{self.time.units}]', ylabel=f'Signal [{self.signal.units}]')
            ax.legend()

            if show:
                plt.show()

    def get_properties(self) -> List[str]:
        """Returns key detector properties formatted for display."""
        return [
            ["Numerical aperture", f"{self.NA:.2f~#P}"],
            ["Phi angle", f"{self.phi_angle:.2f~#P}"],
            ["Theta angle", f"{self.gamma_angle:.2f~#P}"],
            ["Sampling Frequency", f"{self.sampling_freq:.2f~#P}"],
            ["Noise Level", f"{self.noise_level:.2f~#P}"],
            ["Baseline Shift Amplitude", f"{self.baseline_shift:.2f~#P}"],
            ["Saturation Level", f"{self.saturation_level:.2f~#P}"],
            ["Responsitivity", f"{self.responsitivity:.2f~#P}"],
            ["Discretization Bins", self.n_bins],
        ]

    def print_properties(self) -> None:
        """Prints detector properties in tabular format."""
        properties = self.get_properties()
        print(f"\nDetector [{self.name}] Properties")
        print(tabulate(properties, headers=["Property", "Value"], tablefmt="grid"))

    def add_to_report(self) -> List:
        """Returns a list of detector attributes formatted for inclusion in a report."""
        return self.get_properties()
