from dataclasses import dataclass, field
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid
from scipy.signal import find_peaks, peak_widths
from FlowCyPy.peak_finder.base_class import BaseClass
from FlowCyPy.units import Quantity, volt, second
import pint_pandas


@dataclass
class Basic(BaseClass):
    """
    A basic peak detector class that identifies peaks in a signal using a threshold-based method.

    Attributes
    ----------
    height_threshold : Quantity, optional
        The minimum height required for a peak to be considered significant.
        Default is `Quantity(0.1, volt)`.
    rel_height : float, optional
        The relative height at which the peak width is measured. Default is `0.5`.

    Methods
    -------
    detect_peaks(detector: pd.DataFrame, compute_area=True)
        Detects peaks in the input signal and computes their properties.

    plot(detector, ax=None, show=True)
        Plots the input signal with detected peaks and their properties.
    """

    height_threshold: Quantity = Quantity(0.0, volt)
    rel_height: float = 0.5

    def detect_peaks(self, detector: pd.DataFrame, compute_area: bool = True) -> Tuple[Quantity, Quantity, Quantity, Optional[Quantity]]:
        """
        Detects peaks in the signal and calculates their properties such as heights, widths, and areas.

        Parameters
        ----------
        detector : pd.DataFrame
            DataFrame with the signal data to detect peaks in.
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
        # Ensure signal and time are from the DataFrame
        signal = detector.dataframe['Signal'].values
        time = detector.dataframe.Time.values

        self.height_threshold = self.height_threshold.to(signal.units)

        # Find peaks in the signal using the height threshold
        peak_indices, _ = find_peaks(signal, height=self.height_threshold.magnitude)

        # Calculate peak properties
        widths_samples, width_heights, left_ips, right_ips = peak_widths(signal, peak_indices, rel_height=self.rel_height)
        dt = time[1] - time[0]
        widths = widths_samples * dt

        _peak_properties = pd.DataFrame({
            'PeakTimes': detector.dataframe.Time[peak_indices].values,
            'Heights': detector.dataframe.Signal[peak_indices].values,
            'Widths': pint_pandas.PintArray(widths, dtype=widths.units),
            'WidthHeights': pint_pandas.PintArray(width_heights, dtype=volt),
            'LeftIPs': pint_pandas.PintArray(left_ips * dt, dtype=dt.units),
            'RightIPs': pint_pandas.PintArray(right_ips * dt, dtype=dt.units),
        })

        if compute_area:
            _peak_properties['Areas'] = self._compute_peak_areas(detector.dataframe, left_ips, right_ips)

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
        cumulative_integral = np.concatenate(([0], cumulative_trapezoid(df['Signal'].values.numpy_data, x=df.Time.values.numpy_data)))


        # Interpolate cumulative integral at left and right interpolated positions
        left_cum_integral = np.interp(left_ips, np.arange(len(df)), cumulative_integral)
        right_cum_integral = np.interp(right_ips, np.arange(len(df)), cumulative_integral)


        # Compute areas under peaks
        areas = right_cum_integral - left_cum_integral

        return pint_pandas.PintArray(areas, dtype=volt * second)

    def plot(self, detector, ax: plt.Axes = None, show: bool = True) -> None:
        """
        Plots the signal with detected peaks and FWHM lines.

        Parameters
        ----------
        detector : pd.DataFrame
            The detector object containing the data to plot.
        ax : plt.Axes, optional
            The matplotlib Axes to plot on. If not provided, a new figure is created.
        show : bool, optional
            Whether to display the plot immediately. Default is True.
        """
        if not hasattr(detector, 'dataframe'):
            raise ValueError("No data available. Please run detect_peaks() first.")

        with plt.style.context('seaborn-darkgrid'):
            ax = detector.dataframe.plot(
                y='Signal', ax=ax, style='-', xlabel=f"Time [{detector.dataframe.index.values.units}]",
                ylabel=f"Signal [{detector.dataframe['Signal'].values.units}]"
            )
            for index, row in detector.peak_properties.iterrows():
                ax.axvline(row['PeakTimes'], color='r', linestyle='--', lw=1)
            if show:
                plt.show()
