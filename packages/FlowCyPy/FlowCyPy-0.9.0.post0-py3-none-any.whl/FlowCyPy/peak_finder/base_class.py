import numpy as np
from FlowCyPy import ureg
import matplotlib.pyplot as plt
from FlowCyPy.joint_plot import PeakPlotter

class BaseClass:
    """
    A base class to handle common functionality for peak detection,
    including area calculation under peaks.
    """

    def get_areas(self, peak_indices: np.ndarray, widths: np.ndarray, signal: np.ndarray, time: np.ndarray) -> np.ndarray:
        """
        Computes the area under each peak.

        Parameters
        ----------
        peak_indices : np.ndarray
            The indices of detected peaks in the signal.
        widths : np.ndarray
            The widths of the detected peaks.
        signal : np.ndarray
            The signal array.
        time : np.ndarray
            The time array corresponding to the signal.
        dt : float
            The time difference between consecutive samples in the signal.

        Returns
        -------
        np.ndarray
            The area under each peak.
        """
        start_idx = np.maximum(0, (peak_indices - widths / (2 * self.dt)).astype(int)).magnitude
        end_idx = np.minimum(len(signal), (peak_indices + widths / (2 * dt)).astype(int)).magnitude

        areas = np.array([
            np.trapz(signal.magnitude[start:end], time.magnitude[start:end])
            for start, end in zip(start_idx, end_idx)
        ]) * ureg.volt * ureg.second

        return areas

    def plot(self, ax: plt.Axes = None):

        plotter = PeakPlotter(
            dataframe=self._data,
            peak_properties=self._peak_properties
        )

        plotter.add_peaks()

        plotter.add_areas()

        plotter.show()