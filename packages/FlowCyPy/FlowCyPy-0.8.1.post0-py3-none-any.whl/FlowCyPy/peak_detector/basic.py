from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from FlowCyPy.peak_detector.base_class import BasePeakDetector
from FlowCyPy.units import Quantity

@dataclass
class Basic(BasePeakDetector):
    """
    A basic peak detector class that identifies peaks in a signal and calculates their properties.

    Parameters
    ----------
    height_threshold : Quantity, optional
        The minimum height required for a peak to be considered significant.
        Default is `Quantity(0.1)`.

    Attributes
    ----------
    _data : pd.DataFrame
        DataFrame containing the signal data.
    _peak_properties : pd.DataFrame
        DataFrame containing properties of the detected peaks.
    """

    height_threshold: Quantity = Quantity(0.1)

    # Internal storage for data
    _data: Optional[pd.DataFrame] = field(init=False, default=None)
    _peak_properties: Optional[pd.DataFrame] = field(init=False, default=None)

    def detect_peaks(
        self,
        signal: Quantity,
        time: Quantity,
        compute_area: bool = True
    ) -> Tuple[Quantity, Quantity, Quantity, Optional[Quantity]]:
        """
        Detects peaks in the signal and calculates their properties such as height, width, and area.

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
        # Standardize units
        signal, time = self._standardize_units(signal, time)

        # Create DataFrame
        df = self._create_dataframe(signal, time)

        # Find peaks
        peak_indices = self._find_peaks(df)

        # Calculate peak properties
        peak_props = self._calculate_peak_properties(df, peak_indices)

        # Compute areas under peaks if required
        if compute_area:
            self._compute_peak_areas(df, peak_props)

        # Store the DataFrames
        self._data = df
        self._peak_properties = peak_props

        # Extract quantities with units
        peak_times_qty = Quantity(peak_props.index.values, time.units)
        heights_qty = Quantity(peak_props['Heights'].values, signal.units)
        widths_qty = Quantity(peak_props['Widths'].values, time.units)
        areas_qty = Quantity(peak_props['Areas'].values, signal.units * time.units) if compute_area else None

        return peak_times_qty, heights_qty, widths_qty, areas_qty

    def _standardize_units(self, signal: Quantity, time: Quantity) -> Tuple[Quantity, Quantity]:
        """
        Standardizes the units of signal and time to common units.

        Parameters
        ----------
        signal : Quantity
            The signal data with units.
        time : Quantity
            The time data with units.

        Returns
        -------
        signal : Quantity
            Signal converted to common units.
        time : Quantity
            Time converted to common units.
        """
        common_signal_unit = signal.max().to_compact().units
        common_time_unit = time.max().to_compact().units

        signal = signal.to(common_signal_unit)
        time = time.to(common_time_unit)

        self.height_threshold = self.height_threshold.to(signal.units)

        return signal, time

    def _create_dataframe(self, signal: Quantity, time: Quantity) -> pd.DataFrame:
        """
        Creates a pandas DataFrame with the signal and time data.

        Parameters
        ----------
        signal : Quantity
            The signal data with units.
        time : Quantity
            The time data with units.

        Returns
        -------
        df : pd.DataFrame
            DataFrame containing the signal data.
        """
        df = pd.DataFrame({'Signal': signal.magnitude}, index=time.magnitude)
        df.index.name = 'Time'
        df.attrs['units'] = {'Signal': str(signal.units), 'Time': str(time.units)}
        return df

    def _find_peaks(self, df: pd.DataFrame) -> np.ndarray:
        """
        Finds peaks in the signal using scipy's find_peaks.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the signal data.

        Returns
        -------
        peak_indices : np.ndarray
            Indices of the detected peaks.
        """
        signal_values = df['Signal'].values
        height = self.height_threshold.magnitude

        peak_indices, _ = find_peaks(signal_values, height=height)
        return peak_indices

    def _calculate_peak_properties(
        self,
        df: pd.DataFrame,
        peak_indices: np.ndarray) -> pd.DataFrame:
        """
        Calculates properties of the detected peaks.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the signal data.
        peak_indices : np.ndarray
            Indices of the detected peaks.

        Returns
        -------
        peak_props : pd.DataFrame
            DataFrame containing properties of the detected peaks.
        """
        # Get peak times and heights
        time_values = df.index.values
        signal_values = df['Signal'].values

        peak_times = time_values[peak_indices]
        heights = signal_values[peak_indices]

        # Calculate widths at half prominence
        widths_samples, width_heights, left_ips, right_ips = peak_widths(
            x=signal_values,
            peaks=peak_indices,
            rel_height=0.5
        )

        dt = np.mean(np.diff(time_values))
        widths = widths_samples * dt

        # Convert left_ips and right_ips to time values
        left_ips_times = np.interp(left_ips, np.arange(len(df)), time_values)
        right_ips_times = np.interp(right_ips, np.arange(len(df)), time_values)

        # Store peak properties in a DataFrame
        peak_props = pd.DataFrame({
            'Heights': heights,
            'Widths': widths,
            'WidthHeights': width_heights,
            'LeftIPs': left_ips_times,
            'RightIPs': right_ips_times
        }, index=peak_times)
        peak_props.index.name = 'PeakTimes'

        # Store units in attrs
        units = df.attrs['units']
        peak_props.attrs['units'] = {
            'Heights': units['Signal'],
            'Widths': units['Time'],
            'WidthHeights': units['Signal'],
            'LeftIPs': units['Time'],
            'RightIPs': units['Time'],
            'Areas': f"{units['Signal']} * {units['Time']}"
        }

        return peak_props

    def _compute_peak_areas(
        self,
        df: pd.DataFrame,
        peak_props: pd.DataFrame):
        """
        Computes the areas under the detected peaks and adds them to the peak properties DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the signal data.
        peak_props : pd.DataFrame
            DataFrame containing properties of the detected peaks.
        """
        # Compute cumulative integral of the signal
        time_values = df.index.values
        signal_values = df['Signal'].values
        cumulative_integral = np.concatenate(([0], cumulative_trapezoid(signal_values, x=time_values)))

        # Interpolate cumulative integral at left and right interpolated positions
        left_cum_integral = np.interp(peak_props['LeftIPs'].values, time_values, cumulative_integral)
        right_cum_integral = np.interp(peak_props['RightIPs'].values, time_values, cumulative_integral)

        # Compute areas under peaks
        areas = right_cum_integral - left_cum_integral

        # Add areas to the peak properties DataFrame
        peak_props['Areas'] = areas
