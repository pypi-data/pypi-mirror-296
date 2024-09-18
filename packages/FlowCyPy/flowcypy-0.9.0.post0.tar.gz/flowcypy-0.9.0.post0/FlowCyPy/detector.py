import numpy as np
from typing import Optional, Union
import matplotlib.pyplot as plt
from FlowCyPy.units import Quantity, volt, watt, degree, second
from FlowCyPy.utils import PropertiesReport
from pydantic.dataclasses import dataclass
from pydantic import field_validator
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
class Detector(PropertiesReport):
    """
    A class representing a signal detector used in flow cytometry.

    The `Detector` class models the behavior of a photodetector, simulating signal acquisition,
    applying noise and baseline shifts, and processing the signal for analysis.
    The class also provides utilities for plotting and generating tabular information about the detector's properties.

    Attributes:
        name (str): The name or identifier of the detector.
        sampling_freq (Quantity): The sampling frequency of the detector, expected in hertz.
        phi_angle (Quantity): The detection angle in degrees.
        numerical_aperture (float): The numerical aperture of the detector, a unitless value.
        gamma_angle (Quantity, optional): The azimuthal detection angle, default is 0 degrees.
        sampling (int, optional): The number of sampling points, default is 100.
        responsitivity (Quantity, optional): Detector's responsivity, default is 1 volt per watt.
        noise_level (Quantity, optional): The noise level in volts, default is 0 volts.
        baseline_shift (Quantity, optional): The baseline shift applied to the signal, default is 0 volts.
        saturation_level (Quantity, optional): The maximum signal level in volts before saturation, default is infinity.
        n_bins (Union[int, str], optional): The number of discretization bins or bit-depth (e.g., '12bit'), default is '12bit'.
    """

    name: str
    sampling_freq: Quantity
    phi_angle: Quantity
    numerical_aperture: float

    gamma_angle: Optional[Quantity] = Quantity(0, degree)
    sampling: Optional[int] = 100
    responsitivity: Optional[Quantity] = Quantity(1, volt / watt)
    noise_level: Optional[Quantity] = Quantity(0.0, volt)
    baseline_shift: Optional[Quantity] = Quantity(0.0, volt)
    saturation_level: Optional[Quantity] = Quantity(np.inf, volt)
    n_bins: Optional[Union[int, str]] = '12bit'


    @field_validator('sampling_freq')
    def validate_sampling_freq(cls, value):
        """
        Validates that the sampling frequency is provided in hertz.

        Args:
            value (Quantity): The sampling frequency to validate.

        Returns:
            Quantity: The validated sampling frequency.

        Raises:
            ValueError: If the sampling frequency is not in hertz.
        """
        if not value.check('Hz'):
            raise ValueError(f"sampling_freq must be in hertz, but got {value.units}")
        return value

    @field_validator('phi_angle', 'gamma_angle')
    def validate_angles(cls, value):
        """
        Validates that the provided angles are in degrees.

        Args:
            value (Quantity): The angle value to validate.

        Returns:
            Quantity: The validated angle.

        Raises:
            ValueError: If the angle is not in degrees.
        """
        if not value.check('degree'):
            raise ValueError(f"Angle must be in degrees, but got {value.units}")
        return value

    @field_validator('responsitivity')
    def validate_responsitivity(cls, value):
        """
        Validates that the detector's responsivity is provided in volts per watt.

        Args:
            value (Quantity): The responsivity value to validate.

        Returns:
            Quantity: The validated responsivity.

        Raises:
            ValueError: If the responsivity is not in volts per watt.
        """
        if not value.check('V / W'):
            raise ValueError(f"Responsitivity must be in volts per watt, but got {value.units}")
        return value

    @field_validator('noise_level', 'baseline_shift', 'saturation_level')
    def validate_voltage_attributes(cls, value):
        """
        Validates that noise level, baseline shift, and saturation level are all in volts.

        Args:
            value (Quantity): The voltage attribute to validate (noise level, baseline shift, or saturation).

        Returns:
            Quantity: The validated voltage attribute.

        Raises:
            ValueError: If the attribute is not in volts.
        """
        if not value.check('volt'):
            raise ValueError(f"Voltage attributes must be in volts, but got {value.units}")
        return value


    def __post_init__(self) -> None:
        """
        Finalizes the initialization of the detector object.

        This method processes the `n_bins` attribute and ensures that all relevant attributes
        are assigned the correct physical units.
        """
        self._process_n_bins()

        # Convert all Quantity attributes to base SI units (without any prefixes)
        for attr_name, attr_value in vars(self).items():
            if isinstance(attr_value, Quantity):
                # Convert the quantity to its base unit (strip prefix)
                setattr(self, attr_name, attr_value)

    def _process_n_bins(self) -> None:
        """
        Processes the `n_bins` attribute to ensure it is an integer representing the number of bins.

        If `n_bins` is provided as a bit-depth string (e.g., '12bit'), it converts it to an integer number of bins.
        If no valid `n_bins` is provided, a default of 100 bins is used.

        Raises:
            ValueError: If `n_bins` is invalid (neither an integer nor a valid bit-depth string).
        """
        if isinstance(self.n_bins, str):
            bit_depth = int(self.n_bins.rstrip('bit'))
            self.n_bins = 2 ** bit_depth

    def init_raw_signal(self, total_time: float) -> None:
        """
        Initializes the raw signal and time arrays for the detector.

        Args:
            total_time (float): The total duration of the signal to simulate (in seconds).

        This method computes the time points based on the sampling frequency and generates a zero-valued
        raw signal array. The raw signal is initialized in volts.
        """
        time_points = int(self.sampling_freq * total_time)

        time = np.linspace(0 * total_time, total_time, time_points)

        self.dataframe = pd.DataFrame(
            data=dict(
                Time=pint_pandas.PintArray(time, dtype=time.units),
                RawSignal=pint_pandas.PintArray(np.zeros_like(time), dtype=volt),
                Signal=pint_pandas.PintArray(np.zeros_like(time), dtype=volt)
            )
        )

    def capture_signal(self) -> None:
        """
        Captures and processes the raw signal.

        This method applies baseline shift, noise, and saturation to the raw signal,
        then discretizes the processed signal into bins and stores the result.
        """
        self.dataframe.Signal = self.dataframe.RawSignal

        self._apply_baseline_and_noise()

        self._apply_saturation()

        self._discretize_signal()

        self.dataframe['Signal'] = self.dataframe['Signal'].pint.to(self.dataframe['Signal'].max().to_compact().units)
        self.dataframe['RawSignal'] = self.dataframe['RawSignal'].pint.to(self.dataframe['RawSignal'].max().to_compact().units)

    def _apply_baseline_and_noise(self) -> None:
        """
        Adds baseline shift and noise to the raw signal.

        The baseline shift is applied as a sinusoidal function of time, and Gaussian noise
        is added to simulate detector imperfections.
        """
        w0 = np.pi / 2 / second
        baseline = self.baseline_shift * np.sin(w0 * self.dataframe.Time)
        noise = self.noise_level * np.random.normal(size=len(self.dataframe))

        self.dataframe.Signal += baseline + noise

    def _apply_saturation(self) -> None:
        """
        Applies a saturation limit to the signal.

        Signal values that exceed the saturation level are clipped to the maximum allowed value.
        """
        clipped = np.clip(self.dataframe.Signal, 0 * volt, self.saturation_level)
        self.dataframe.Signal = pint_pandas.PintArray(clipped, clipped.units)

    def _discretize_signal(self) -> None:
        """
        Discretizes the processed signal into a specified number of bins.

        The signal is mapped to discrete levels, depending on the number of bins (derived from `n_bins`).
        """
        if self.n_bins:
            max_level = self.saturation_level if self.saturation_level.to(volt).magnitude is not np.inf else self.dataframe.Signal.max()

            bins = np.linspace(0 * max_level, max_level, self.n_bins)

            digitized = np.digitize(
                x=self.dataframe.Signal.pint.to(volt).pint.magnitude,
                bins=bins.to(volt).magnitude
            ) - 1

            self.dataframe.Signal = pint_pandas.PintArray(bins[digitized], volt)

    def plot(self, show: bool = True, figure_size: tuple = None, color: str = 'C0', ax: plt.Axes = None) -> None:
        """
        Plots the processed signal over time.

        Args:
            show (bool, optional): If True, display the plot immediately. Default is True.
            figure_size (tuple, optional): The size of the figure in inches (width, height). Default is None.
            color (str, optional): The color of the plotted signal line. Default is 'C0'.

        This method visualizes the processed signal as a function of time.
        """
        with plt.style.context(mps):
            ax = self.dataframe.plot(x='Time', y=['Signal'], ax=ax, color=color, figsize=figure_size)
            ax.set_xlabel(f"Time [{self.dataframe.Time.values.units}]")
            ax.set_ylabel(f"Signal [{self.dataframe.Signal.values.units}]")

            if show:
                plt.show()
