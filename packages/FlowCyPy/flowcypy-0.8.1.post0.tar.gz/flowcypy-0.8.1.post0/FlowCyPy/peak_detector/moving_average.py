from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np

from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from FlowCyPy.peak_detector.base_class import BasePeakDetector
from FlowCyPy.units import Quantity
import pandas as pd
import pint_pandas
from MPSPlots.styles import mps
import matplotlib.pyplot as plt

from FlowCyPy.units import Quantity, second, volt, microsecond
PT_ = pint_pandas.PintType
ureg = PT_.ureg
ureg.setup_matplotlib()

@dataclass
class MovingAverage(BasePeakDetector):
    """
    Detects peaks in a signal using a moving average algorithm.
    A peak is identified when the signal exceeds the moving average by a defined threshold.

    Attributes
    ----------
    threshold : Quantity, optional
        The minimum difference between the signal and its moving average required to detect a peak.
        Default is `Quantity(0.2)`.
    window_size : Quantity, optional
        The window size for calculating the moving average.
        Default is `Quantity(500)`.
    min_peak_distance : Quantity, optional
        The minimum distance between detected peaks.
        Default is `Quantity(0.1)`.
    rel_height : float, optional
        The relative height at which the peak width is measured. Default is `0.5` (half-height).

    Methods
    -------
    detect_peaks(signal, time, compute_area=True)
        Detects peaks and calculates their properties from the input signal.

    plot()
        Plots the signal with detected peaks and FWHM lines.
    """

    threshold: Quantity = None
    window_size: Quantity = Quantity(5, microsecond)
    min_peak_distance: Quantity = None
    rel_height: float = 0.8

    def compute_moving_average(self, dataframe: pd.DataFrame) -> None:
        dt = dataframe.index.values[1] - dataframe.index.values[0]

        window_size_samples = int(np.ceil(self.window_size / dt))

        moving_avrg = dataframe['Signal'].rolling(window=window_size_samples, center=True).mean()

        # Handle NaN values resulting from rolling mean
        moving_avrg = moving_avrg.bfill().ffill()

        dataframe['MovingAverage'] = pint_pandas.PintArray(moving_avrg, dtype=dataframe['Signal'].values.units)

        # Calculate the difference between signal and moving average
        dataframe['Difference'] = dataframe['Signal'] - dataframe['MovingAverage']

    def detect_peaks(self, detector: pd.DataFrame, compute_area: bool = True) -> Tuple[Quantity, Quantity, Quantity, Optional[Quantity]]:
        """
        Detects peaks in the signal using a moving average and a threshold.

        Parameters
        ----------
        signal : Quantity
            The signal data to detect peaks in, with units.
        time : Quantity
            The time array corresponding to the signal, with units.
        compute_area : bool, optional
            If True, computes the area under each peak. Default is True.

        Returns
        -------
        peak_times : Quantity
            The times at which peaks occur.
        heights : Quantity
            The heights of the detected peaks.
        widths : Quantity
            The widths of the detected peaks.
        areas : Quantity or None
            The areas under each peak, if `compute_area` is True.
        """
        signal = detector.dataframe['Signal'].values
        time = detector.dataframe.index.values

        if self.threshold is not None:
            self.threshold = self.threshold.to(signal.units)

        self.window_size = self.window_size.to(time.units)

        if self.min_peak_distance is not None:
            self.min_peak_distance = self.min_peak_distance.to(time.units)

        # Calculate the moving average
        dt = detector.dataframe.index[1] - detector.dataframe.index[0]

        self.compute_moving_average(detector.dataframe)

        # Find peaks in the difference signal
        peak_indices, _ = find_peaks(
            detector.dataframe['Difference'].values,
            height=None if self.threshold is None else self.threshold.magnitude,
            distance=None if self.min_peak_distance is None else int(np.ceil(self.min_peak_distance / dt))
        )

        # Calculate peak properties
        widths_samples, width_heights, left_ips, right_ips = peak_widths(
            detector.dataframe['Difference'].values,
            peak_indices,
            rel_height=self.rel_height
        )

        # Convert widths from samples to time units
        widths = widths_samples * dt
        peak_times = detector.dataframe.index.values[peak_indices]
        heights = detector.dataframe['Signal'].values[peak_indices]

        _peak_properties = pd.DataFrame({
                'PeakTimes': pint_pandas.PintArray(peak_times, dtype=peak_times.units),
                'Heights': pint_pandas.PintArray(heights, dtype=volt),
                'Widths': pint_pandas.PintArray(widths, dtype=widths.units),
                'WidthHeights': pint_pandas.PintArray(width_heights, dtype=volt),
                'LeftIPs': pint_pandas.PintArray(left_ips * dt, dtype=dt.units),
                'RightIPs': pint_pandas.PintArray(right_ips * dt, dtype=dt.units),
        })

        # Compute areas under peaks
        if compute_area:
            _peak_properties['Areas'] = self._compute_peak_areas(detector.dataframe, left_ips, right_ips)

        # self._peak_properties = pd.DataFrame(peak_data)
        _peak_properties.set_index('PeakTimes', inplace=True)
        _peak_properties['PeakTimes'] = _peak_properties.index

        # Store the full data DataFrame
        detector.peak_properties = _peak_properties

    def _compute_peak_areas(
        self,
        df: pd.DataFrame,
        left_ips: np.ndarray,
        right_ips: np.ndarray) -> np.ndarray:
        """
        Computes the areas under the detected peaks using vectorized operations.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the signal data.
        left_ips : np.ndarray
            Left interpolated positions of peak widths (fractional indices).
        right_ips : np.ndarray
            Right interpolated positions of peak widths (fractional indices).

        Returns
        -------
        areas : np.ndarray
            Areas under each peak.
        """
        # Compute cumulative integral of the signal
        cumulative_integral = np.concatenate(([0], cumulative_trapezoid(df['Signal'].values.numpy_data, x=df.index.values.numpy_data)))


        # Interpolate cumulative integral at left and right interpolated positions
        left_cum_integral = np.interp(left_ips, np.arange(len(df)), cumulative_integral)
        right_cum_integral = np.interp(right_ips, np.arange(len(df)), cumulative_integral)


        # Compute areas under peaks
        areas = right_cum_integral - left_cum_integral

        return pint_pandas.PintArray(areas, dtype=volt * second)

    def plot(self, detector, ax: plt.Axes = None, show: bool = True) -> None:

        if not hasattr(detector, 'dataframe'):
            self.detect_peaks(detector=detector)

        with plt.style.context(mps):
            ax = detector.dataframe.plot(
                y=['Signal', 'MovingAverage', 'Difference'],
                style=['-', '--', '--'],
                ax=ax,
                ylabel=f'{detector.name} signal [{detector.dataframe.Signal.values.units}]',
                xlabel=f'Time [{detector.dataframe.index.values.units}]'
            )

            for index, row in detector.peak_properties.iterrows():
                ax.axvline(row['PeakTimes'], color='r', linestyle='--', lw=1, label='Peak')

            if show:
                plt.show()