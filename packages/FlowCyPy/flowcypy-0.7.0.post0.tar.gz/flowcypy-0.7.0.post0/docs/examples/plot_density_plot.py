"""
Flow Cytometry Simulation and 2D Hexbin Plot of Scattering Intensities
======================================================================

This script simulates a flow cytometer experiment using the FlowCyPy library. It analyzes pulse signals from two
detectors and generates a 2D hexbin plot of the scattering intensities. Flow cytometry is a technique to analyze
the physical and chemical properties of particles as they flow through a laser beam.

Steps:
1. Define the flow parameters (e.g., speed, area).
2. Create particle size and refractive index distributions.
3. Set up a laser source and configure detectors.
4. Simulate the flow cytometry experiment.
5. Analyze pulse signals from both detectors.
6. Plot a 2D density plot of the scattering intensities.
"""

# Import necessary libraries and modules
import numpy as np
from FlowCyPy import FlowCytometer, ScattererDistribution, Analyzer, Detector, Source, FlowCell, Plotter
from FlowCyPy import distribution
from FlowCyPy.peak_detector import BasicPeakDetector
from FlowCyPy.population import Population
from FlowCyPy.units import (
    microsecond, micrometer, meter, refractive_index_unit, milliliter, millisecond, nanometer,
    milliwatt, degree, volt, watt, megahertz, particle, second
)

# Set random seed for reproducibility
np.random.seed(30)

# Step 1: Define Flow Parameters
flow = FlowCell(
    flow_speed=7.56 * meter / second / 30,       # Flow speed: ~7.56 meters per second divided by 30
    flow_area=(10 * micrometer) ** 2,            # Flow area: 10 micrometers by 10 micrometers
    total_time=10 * millisecond                  # Total simulation time: 10 milliseconds
)

# %%
# Step 2: Define Particle Size and Refractive Index Distributions
ev_size = distribution.Normal(
    mean=200 * nanometer,                        # Mean particle size: 200 nanometers
    std_dev=50 * nanometer                       # Standard deviation of particle size: 10 nanometers
)

ev_ri = distribution.Normal(
    mean=1.39 * refractive_index_unit,           # Mean refractive index: 1.39
    std_dev=0.1 * refractive_index_unit          # Standard deviation of refractive index: 0.01
)

ev = Population(
    size=ev_size,                                  # Particle size distribution
    refractive_index=ev_ri,                        # Refractive index distribution
    concentration=1.8e+9 * particle / milliliter,  # Concentration: 1.8e9 particles per milliliter divided by 3
    name='EV'                                      # Name of population
)

scatterer_distribution = ScattererDistribution(
    flow=flow,                                   # Flow parameters
    populations=[ev]                             # List of populations (here just EVs)
)

# Plot the scatterer distribution
scatterer_distribution.plot()

# %%
# Step 3: Set up the Laser Source
source = Source(
    NA=0.1,                                      # Numerical aperture of the laser
    wavelength=800 * nanometer,                  # Laser wavelength: 800 nanometers
    optical_power=20 * milliwatt                 # Laser optical power: 2 milliwatts
)

# Step 4: Set up Detectors
detector_0 = Detector(
    phi_angle=90 * degree,                       # Detector angle: 90 degrees (Side scatter)
    NA=1.2,                                      # Numerical aperture: 1.2
    name='Side',                                 # Detector name: Side
    responsitivity=1 * volt / watt,              # Responsitivity: 1 volt per watt
    acquisition_frequency=10 * megahertz,        # Sampling frequency: 10 MHz
    noise_level=0 * volt,                        # Noise level: No noise
    baseline_shift=0.00 * volt,                  # Baseline shift: None
    saturation_level=100 * volt,                 # Saturation level: 100 volts
    n_bins='14bit'                               # Discretization bins: 14-bit
)

detector_1 = Detector(
    phi_angle=180 * degree,                      # Detector angle: 180 degrees (Forward scatter)
    NA=1.2,                                      # Numerical aperture: 1.2
    name='Front',                                # Detector name: Front
    responsitivity=1 * volt / watt,              # Responsitivity: 1 volt per watt
    acquisition_frequency=10 * megahertz,        # Sampling frequency: 10 MHz
    noise_level=0 * volt,                        # Noise level: No noise
    baseline_shift=0.00 * volt,                  # Baseline shift: None
    saturation_level=100 * volt,                 # Saturation level: 100 volts
    n_bins='14bit'                               # Discretization bins: 14-bit
)

# Step 5: Simulate Flow Cytometry Experiment
cytometer = FlowCytometer(
    coupling_mechanism='mie',                    # Scattering mechanism: Mie scattering
    source=source,                               # Laser source
    scatterer_distribution=scatterer_distribution,  # Particle size and refractive index distributions
    detectors=[detector_0, detector_1]           # List of detectors
)

# Run the simulation to generate scattering signals
cytometer.simulate_pulse()

# Plot the scattering signals for both detectors
cytometer.plot()

# %%
# Step 6: Analyze the Pulse Signals
analyzer = Analyzer(
    detector_0, detector_1,                      # Two detectors (Side scatter and Forward scatter)
    algorithm=BasicPeakDetector()                # Peak detection algorithm: BasicPeakDetector
)

# Analyze the signals without computing the peak area
analyzer.run_analysis(compute_peak_area=False)

# Plot the analyzed pulse signals
analyzer.plot()

# %%
# Step 7: Extract and Plot Coincidence Data
datasets = analyzer.get_coincidence_dataset(
    coincidence_margin=0.1 * microsecond         # Time margin for detecting coincident pulses: 0.1 microseconds
)

# Step 8: Plot the 2D Density Plot of Scattering Intensities
plotter = Plotter(
    dataset_0=datasets[0],                       # Data from detector 0 (Side scatter)
    dataset_1=datasets[1]                        # Data from detector 1 (Forward scatter)
)

# Plot the density plot
plotter.plot()
