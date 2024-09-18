#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Callable
from MPSPlots.styles import mps
from dataclasses import dataclass
from FlowCyPy.scatterer import Scatterer
from FlowCyPy.detector import Detector
from FlowCyPy.source import Source
from tabulate import tabulate
import pandas as pd
import pint_pandas


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

@dataclass
class FlowCytometer:
    """
    A class to simulate flow cytometer signals for Forward Scatter (FSC) and Side Scatter (SSC) channels.

    This class models the particle distribution, flow characteristics, and detector configurations to
    simulate the signal generated as particles pass through the flow cytometer's laser.

    Attributes
    ----------
    scatterer : Scatterer
        The distribution of particle sizes which affects scattering signals.
    source : Source
        The laser source object representing the illumination scheme.
    detectors : List[Detector]
        List of `Detector` objects representing the detectors in the system.

    Methods
    -------
    simulate_pulse()
        Simulates the signal pulses for FSC and SSC channels based on particle distribution and flow.
    plot()
        Plots the simulated signals for each detector channel.
    print_properties()
        Displays the key properties of the flow cytometer and its detectors.
    """
    scatterer: Scatterer
    source: Source
    detectors: List[Detector]
    coupling_mechanism: str = 'mie'

    def __post_init__(self) -> None:
        assert len(self.detectors) == 2, 'For now, FlowCytometer can only take two detectors for the analysis.'
        assert self.detectors[0].name != self.detectors[1].name, 'Both detectors cannot have the same name'

    def print_properties(self) -> None:
        """Displays the core properties of the flow cytometer and its detectors using the `tabulate` library."""
        self.scatterer.print_properties()
        print("\nFlowCytometer Properties")

        self.source.print_properties()

        for detector in self.detectors:
            detector.print_properties()

    def simulate_pulse(self) -> None:
        """
        Simulates the signal pulses for the FSC and SSC channels by generating Gaussian pulses for
        each particle event and distributing them across the detectors.
        """
        logging.debug("Starting pulse simulation.")

        _centers, _widths = self._generate_pulse_parameters()

        columns = pd.MultiIndex.from_product(
            [[p.name for p in self.detectors], ['Centers', 'Widths', 'Heights']]
        )

        self.pulse_dataframe = pd.DataFrame(columns=columns)

        centers = _centers[:, np.newaxis]
        widths = _widths[:, np.newaxis]

        detection_mechanism = self._get_detection_mechanism()

        for detector in self.detectors:
            self.pulse_dataframe[detector.name, 'Centers'] = pint_pandas.PintArray(_centers, dtype=centers.units)
            self.pulse_dataframe[detector.name, 'Widths'] = pint_pandas.PintArray(_widths, dtype=widths.units)

            detector.init_raw_signal(total_time=self.scatterer.flow_cell.total_time)

            _heights = detection_mechanism(
                source=self.source,
                detector=detector,
                scatterer=self.scatterer
            )

            # Broadcast the time array to the shape of (number of signals, len(detector.time))
            time_grid = np.expand_dims(detector.dataframe.Time.values.numpy_data, axis=0) * centers.units


            b = np.exp(- (time_grid - centers) ** 2 / (2 * widths ** 2))

            # Compute the Gaussian for each height, center, and width using broadcasting
            gaussians = _heights[:, np.newaxis] * b

            # Sum all the Gaussians and add them to the detector.raw_signal
            detector.dataframe.RawSignal += np.sum(gaussians, axis=0)

        for detector in self.detectors:
            detector.capture_signal()

        self._log_statistics()

    def _log_statistics(self) -> None:
        """
        Logs key statistics about the simulated pulse events for each detector using tabulate for better formatting.
        Includes total events, average time between events, gfirst and last event times, and minimum time between events.
        """
        total_events = 0
        table_data = []  # List to store table data for each detector

        logging.info("\n=== Simulation Statistics Summary ===")

        # Iterate through each detector to calculate statistics
        for detector in self.detectors:
            centers = self.pulse_dataframe[detector.name, 'Centers']
            num_events = len(centers)
            total_events += num_events

            # Calculate average and minimum time between events if more than one event is detected
            if num_events > 1:
                centers_sorted = centers.sort_values()
                time_diffs = centers_sorted.diff().dropna()  # Compute time differences between events
                avg_time_between_events = time_diffs.mean()
                min_time_between_events = time_diffs.min()
            else:
                avg_time_between_events = "N/A"
                min_time_between_events = "N/A"

            # Get first and last event times
            first_event_time = centers.min() if num_events > 0 else "N/A"
            last_event_time = centers.max() if num_events > 0 else "N/A"

            # Append detector statistics to table data
            table_data.append([
                detector.name,                                  # Detector name
                num_events,                                     # Number of events
                f"{first_event_time.to_compact():.4~P}",        # First event time
                f"{last_event_time.to_compact():.4~P}",         # Last event time
                f"{avg_time_between_events.to_compact():.4~P}" if avg_time_between_events != "N/A" else "N/A",  # Average time between events
                f"{min_time_between_events.to_compact():.4~P}" if min_time_between_events != "N/A" else "N/A"   # Minimum time between events
            ])

        # Format the table using tabulate for better readability
        headers = ["Detector", "Number of Events", "First Event Time", "Last Event Time", "Avg Time Between Events", "Min Time Between Events"]
        formatted_table = tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".3f")

        # Log the formatted table
        logging.info("\n" + formatted_table)

        # Log total events across all detectors
        logging.info(f"\nTotal number of events detected across all detectors: {total_events}")


    def _get_detection_mechanism(self) -> Callable:
        """
        Generates coupling factors for the scatterer sizes based on the selected coupling mechanism.

        Returns
        -------
        Callable
            The generated coupling factors for the scatterer sizes.
        """
        from FlowCyPy import coupling_mechanism

        # Determine which coupling mechanism to use and compute the corresponding factors
        match self.coupling_mechanism.lower():
            case 'rayleigh':
                return coupling_mechanism.rayleigh.compute_detected_signal
            case 'uniform':
                return coupling_mechanism.uniform.compute_detected_signal
            case 'mie':
                return coupling_mechanism.mie.compute_detected_signal
            case 'empirical':
                return coupling_mechanism.empirical.compute_detected_signal
            case _:
                raise ValueError("Invalid coupling mechanism. Choose 'rayleigh' or 'uniform'.")

    def _generate_pulse_parameters(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates random parameters for a Gaussian pulse, including the center and width.

        Returns
        -------
        center : np.ndarray
            The center of the pulse in time.
        width : np.ndarray
            The width of the pulse (standard deviation of the Gaussian, in seconds).
        """
        centers = np.concatenate([
            p.time_positions for p in self.scatterer.populations
        ])

        widths = self.source.waist / self.scatterer.flow_cell.flow_speed * np.ones(centers.size)

        return centers, widths

    def plot(self, figure_size: tuple = (10, 6)) -> None:
        """Plots the signals generated for each detector channel."""
        logging.info(f"Plotting the signal for the different channels.")

        with plt.style.context(mps):
            fig, axes = plt.subplots(2, 1, figsize=figure_size, sharex=True)

            for ax, detector in zip(axes, self.detectors):
                detector.plot(ax=ax, show=False)

                ax.vlines(
                    x=self.pulse_dataframe[detector.name, 'Centers'],
                    ymin=0,
                    ymax=1,
                    transform=ax.get_xaxis_transform(),
                    color='red',
                    lw=1,
                    linestyle='--'
                )

            plt.show()
