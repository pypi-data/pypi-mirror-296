"""
Simulating and Analyzing Flow Cytometer Signals
===============================================

This script simulates flow cytometer signals using the `FlowCytometer` class and analyzes the results using
the `PulseAnalyzer` class from the FlowCyPy library. The signals generated (forward scatter and side scatter)
provide insights into the physical properties of particles passing through the laser beam.

Workflow:
---------
1. Define a particle size distribution using `ScattererDistribution`.
2. Simulate flow cytometer signals using `FlowCytometer`.
3. Analyze the forward scatter signal with `PulseAnalyzer` to extract features like peak height, width, and area.
4. Visualize the generated signals and display the extracted pulse features.
"""

# %%
# Step 1: Import necessary modules from FlowCyPy
from FlowCyPy import FlowCytometer, ScattererDistribution, Detector, Source, FlowCell
from FlowCyPy import distribution
from FlowCyPy.population import Population
from FlowCyPy.units import nanometer, refractive_index_unit, milliliter, particle

# %%
# Step 2: Define flow parameters
# ------------------------------
# Set the flow speed to 80 micrometers per second and a flow area of 1 square micrometer, with a total simulation time of 1 second.
flow = FlowCell(
    flow_speed=80e-6,           # Flow speed: 80 micrometers per second
    flow_area=1e-6,             # Flow area: 1 square micrometer
    total_time=1.0              # Total simulation time: 1 second
)

# %%
# Step 3: Define the particle size distribution
# ---------------------------------------------
# Use a normal size distribution with a mean size of 200 nanometers and a standard deviation of 10 nanometers.
# This represents the population of scatterers (particles) that will interact with the laser source.
ev_size = distribution.Normal(
    mean=200 * nanometer,       # Mean particle size: 200 nanometers
    std_dev=10 * nanometer      # Standard deviation: 10 nanometers
)

ev_ri = distribution.Normal(
    mean=1.39 * refractive_index_unit,    # Mean refractive index: 1.39
    std_dev=0.01 * refractive_index_unit  # Standard deviation: 0.01
)

ev = Population(
    size=ev_size,               # Particle size distribution
    refractive_index=ev_ri,     # Refractive index distribution
    concentration=1.8e+6 * particle / milliliter,  # Particle concentration: 1.8 million particles per milliliter
    name='EV'                   # Name of the particle population: Extracellular Vesicles (EV)
)

scatterer_distribution = ScattererDistribution(
    flow=flow,                  # Flow parameters
    populations=[ev]            # List of populations (only EVs in this case)
)

# Plot the scatterer distribution
scatterer_distribution.plot()

# %%
# Step 4: Define the laser source
# -------------------------------
# Set up a laser source with a wavelength of 1550 nm, optical power of 200 mW, and a numerical aperture of 0.3.
source = Source(
    NA=0.3,                     # Numerical aperture: 0.3
    wavelength=1550e-9,          # Laser wavelength: 1550 nm
    optical_power=200e-3         # Optical power: 200 milliwatts
)

# Step 5: Define the detector
# ---------------------------
# The detector captures the scattered light. It is positioned at 90 degrees relative to the incident light beam
# and configured with a numerical aperture of 0.4 and responsitivity of 1.
detector = Detector(
    phi_angle=90,               # Detector angle: 90 degrees (Side Scatter)
    NA=0.4,                     # Numerical aperture of the detector
    name='first detector',       # Detector name
    responsitivity=1,            # Responsitivity of the detector (light to signal conversion efficiency)
    acquisition_frequency=1e4,   # Sampling frequency: 10,000 Hz
    noise_level=0e-2,            # Noise level: 1 millivolt
    baseline_shift=0.01,         # Baseline shift: 0.01 volts
    saturation_level=1e30,       # Saturation level: Large enough to avoid saturation
    n_bins=1024                  # Number of bins for signal discretization: 1024
)

# Step 6: Simulate Flow Cytometer Signals
# ---------------------------------------
# Create a FlowCytometer instance to simulate the signals generated as particles pass through the laser beam.
cytometer = FlowCytometer(
    coupling_mechanism='empirical',        # Scattering model: Empirical (Rayleigh scattering for small particles)
    source=source,                         # Laser source
    scatterer_distribution=scatterer_distribution,  # Particle size distribution
    detectors=[detector]                   # List of detectors used in the simulation
)

# Simulate the pulse signals generated from the interaction between particles and the laser.
cytometer.simulate_pulse()

# %%
# Step 7: Analyze and Visualize Results
# -------------------------------------
# Display the properties of the simulated cytometer setup, including flow speed and laser power.
cytometer.print_properties()

# Plot the simulated signals for the detector.
cytometer.plot()

"""
Summary:
--------
This script simulates flow cytometer signals, processes them to detect peaks in the forward scatter channel,
and extracts important features. The process is visualized through signal plots, and key properties are displayed.
"""
