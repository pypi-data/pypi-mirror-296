"""
Flow Cytometry Simulation and 2D Density Plot of Scattering Intensities
=======================================================================

This example simulates a flow cytometer experiment using the FlowCyPy library,
analyzes pulse signals from two detectors, and generates a 2D density plot of the scattering intensities.

Steps:
1. Set flow parameters and particle size distributions.
2. Set up the laser source and detectors.
3. Simulate the flow cytometry experiment.
4. Analyze pulse signals and generate a 2D density plot.
"""

# Import necessary libraries and modules
import numpy as np
from FlowCyPy import FlowCytometer, ScattererDistribution, Analyzer, Detector, Source, FlowCell, Plotter
from FlowCyPy import distribution
from FlowCyPy.peak_detector import BasicPeakDetector
from FlowCyPy.population import Population
from FlowCyPy.units import (
    microsecond, micrometer, meter, refractive_index_unit, milliliter, second,
    millisecond, nanometer, milliwatt, degree, volt, watt, megahertz, particle
)

# Set random seed for reproducibility
np.random.seed(3)

# Step 1: Define Flow Parameters
flow = FlowCell(
    flow_speed=7.56 * meter / second,        # Flow speed: 7.56 meters per second
    flow_area=(10 * micrometer) ** 2,        # Flow area: 10 x 10 micrometers
    total_time=1.0 * millisecond             # Total simulation time: 0.3 milliseconds
)

# %%
# Step 2: Define Particle Size and Refractive Index Distributions
lp_size = distribution.RosinRammler(
    characteristic_size=200 * nanometer,     # Characteristic particle size: 200 nanometers
    spread=1.3                                 # Spread of particle size distribution
)
ev_size = distribution.RosinRammler(
    characteristic_size=50 * nanometer,      # Characteristic particle size: 50 nanometers
    spread=1.7                                 # Spread of particle size distribution
)

# Plot particle size distributions for Liposomes
lp_size.plot()

# %%
# Plot particle size distributions for Extracellular Vesicles
ev_size.plot()

# %%
lp_ri = distribution.Normal(
    mean=1.45 * refractive_index_unit,       # Mean refractive index for Liposomes: 1.45
    std_dev=0.05 * refractive_index_unit     # Standard deviation of refractive index: 0.01
)
ev_ri = distribution.Normal(
    mean=1.39 * refractive_index_unit,       # Mean refractive index for EVs: 1.39
    std_dev=0.05 * refractive_index_unit     # Standard deviation of refractive index: 0.01
)

# Step 3: Create Populations (Extracellular Vesicles and Liposomes)
ev = Population(
    size=ev_size,                            # Particle size distribution for EVs
    refractive_index=ev_ri,                  # Refractive index distribution for EVs
    concentration=1e+9 * particle / milliliter,  # Concentration: 1e9 particles per milliliter
    name='EV'                                # Name of population
)
lp = Population(
    size=lp_size,                            # Particle size distribution for Liposomes
    refractive_index=lp_ri,                  # Refractive index distribution for Liposomes
    concentration=1e+9 * particle / milliliter,  # Concentration: 1e9 particles per milliliter
    name='LP'                                # Name of population
)

scatterer_distribution = ScattererDistribution(
    flow=flow,                               # Flow parameters
    populations=[ev, lp]                     # List of particle populations
)

# Plot scatterer distribution
scatterer_distribution.plot()

# %%
# Step 4: Set up the Laser Source
source = Source(
    NA=0.2,                                  # Numerical aperture of the laser: 0.2
    wavelength=800 * nanometer,              # Laser wavelength: 800 nanometers
    optical_power=20 * milliwatt             # Laser optical power: 20 milliwatts
)

# Step 5: Configure Detectors
detector_0 = Detector(
    name='side',                             # Detector name: Side scatter detector
    phi_angle=90 * degree,                   # Angle: 90 degrees (Side Scatter)
    NA=1.2,                                  # Numerical aperture: 1.2
    responsitivity=1 * volt / watt,          # Responsitivity: 1 volt per watt
    acquisition_frequency=10 * megahertz,    # Sampling frequency: 10 MHz
    noise_level=0 * volt,                    # Noise level: 0 volts
    saturation_level=100 * volt,             # Saturation level: 100 volts
    n_bins='14bit'                           # Discretization bins: 14-bit resolution
)

detector_1 = Detector(
    name='forward',                          # Detector name: Forward scatter detector
    phi_angle=180 * degree,                  # Angle: 180 degrees (Forward Scatter)
    NA=1.2,                                  # Numerical aperture: 1.2
    responsitivity=1 * volt / watt,          # Responsitivity: 1 volt per watt
    acquisition_frequency=10 * megahertz,    # Sampling frequency: 10 MHz
    noise_level=0 * volt,                    # Noise level: 0 volts
    saturation_level=100 * volt,             # Saturation level: 100 volts
    n_bins='14bit'                           # Discretization bins: 14-bit resolution
)

# Step 6: Simulate Flow Cytometry Experiment
cytometer = FlowCytometer(
    coupling_mechanism='mie',                # Use Mie scattering for particle simulation
    source=source,                           # Laser source
    scatterer_distribution=scatterer_distribution,  # Particle size and refractive index distribution
    detectors=[detector_0, detector_1]       # Two detectors: Side scatter and Forward scatter
)

# Run the simulation
cytometer.simulate_pulse()

# Plot the results of scattering signals from both detectors
cytometer.plot()

# %%
# Step 7: Analyze Pulse Signals
analyzer = Analyzer(
    detector_0, detector_1,                  # Two detectors: Side scatter and Forward scatter
    algorithm=BasicPeakDetector()            # Peak detection algorithm: BasicPeakDetector
)

# Analyze pulse signals
analyzer.run_analysis(compute_peak_area=False)  # Analysis with no peak area computation

# Plot the analyzed pulse signals
analyzer.plot()

# %%
# Step 8: Extract and Plot Coincidence Data
datasets = analyzer.get_coincidence_dataset(
    coincidence_margin=0.1 * microsecond     # Margin for detecting coincident pulses: 0.1 microsecond
)

# Step 9: Plot the 2D Density Plot of Scattering Intensities
plotter = Plotter(
    dataset_0=datasets[0],                   # Processed data from the first detector
    dataset_1=datasets[1]                    # Processed data from the second detector
)

# Plot the 2D density plot
plotter.plot()
