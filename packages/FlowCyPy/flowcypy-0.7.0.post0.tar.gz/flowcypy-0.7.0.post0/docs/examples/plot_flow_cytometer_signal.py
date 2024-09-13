"""
Simulating Flow Cytometer Signals with Rayleigh Scattering
==========================================================

This script simulates signals from a flow cytometer using Rayleigh scattering to model the interaction
of particles with a laser beam. It demonstrates how to generate Forward Scatter (FSC) and Side Scatter (SSC) signals
using FlowCyPy and visualize the results.

Steps:
1. Define the flow parameters and particle size distribution.
2. Set up the laser source and detectors.
3. Simulate the flow cytometer signals.
4. Visualize and analyze the signals from FSC and SSC detectors.
"""

# Step 1: Import the necessary libraries
import numpy as np
from FlowCyPy import FlowCytometer, ScattererDistribution, Detector, Source, FlowCell
from FlowCyPy import distribution
from FlowCyPy.population import Population
from FlowCyPy.units import (
    refractive_index_unit, milliliter, particle, nanometer
)

# Step 2: Define the flow parameters
# ----------------------------------
# Flow speed is set to 80 micrometers per second, with a flow area of 1 square micrometer and a total simulation time of 1 second.
flow = FlowCell(
    flow_speed=80e-6,            # Flow speed: 80 micrometers per second
    flow_area=1e-6,              # Flow area: 1 square micrometer
    total_time=1.0               # Total flow time: 1 second
)

flow.print_properties()

# Step 3: Define the particle size distribution
# ---------------------------------------------
# We define a normal distribution for particle sizes with a mean of 200 nm, standard deviation of 10 nm,
# and a refractive index of 1.39 with a small variation of 0.01.
ev_size = distribution.Normal(
    mean=200 * nanometer,        # Mean particle size: 200 nanometers
    std_dev=10 * nanometer       # Standard deviation of particle size: 10 nanometers
)

ev_ri = distribution.Normal(
    mean=1.39 * refractive_index_unit,  # Mean refractive index: 1.39
    std_dev=0.01 * refractive_index_unit  # Standard deviation: 0.01
)

ev = Population(
    size=ev_size,                # Particle size distribution
    refractive_index=ev_ri,      # Refractive index distribution
    concentration=1.8e+6 * particle / milliliter,  # Concentration: 1.8e6 particles per milliliter
    name='EV'                    # Population name: Extracellular Vesicles (EV)
)

scatterer_distribution = ScattererDistribution(
    flow=flow,                   # Flow parameters
    populations=[ev]             # List of populations
)

scatterer_distribution.plot()
scatterer_distribution.print_properties()

# Step 4: Set up the light source
# -------------------------------
# A laser with a wavelength of 1550 nm, optical power of 2 mW, and a numerical aperture of 0.4 is used.
source = Source(
    NA=0.4,                       # Numerical aperture: 0.4
    wavelength=1550e-9,            # Wavelength: 1550 nm
    optical_power=2e-3             # Optical power: 2 mW
)

# Step 5: Set up the detectors
# ----------------------------
# Two detectors are used: Forward Scatter (FSC) and Side Scatter (SSC). Each detector is configured
# with its own numerical aperture, responsitivity, noise level, and acquisition frequency.
detector_fsc = Detector(
    name='FSC',                   # Forward Scatter detector
    NA=0.2,                       # Numerical aperture: 0.2
    phi_angle=180,                # Angle: 180 degrees for forward scatter
    acquisition_frequency=1e3,    # Sampling frequency: 1000 Hz
    noise_level=1e-9,             # Noise level: 1e-9 volts
    saturation_level=10,          # Saturation level: 10 volts
    n_bins=512,                   # Number of discretization bins: 512
    responsitivity=1              # Responsitivity: 1
)

detector_ssc = Detector(
    name='SSC',                   # Side Scatter detector
    NA=0.2,                       # Numerical aperture: 0.2
    phi_angle=90,                 # Angle: 90 degrees for side scatter
    acquisition_frequency=1e3,    # Sampling frequency: 1000 Hz
    noise_level=1e-9,             # Noise level: 1e-9 volts
    saturation_level=10,          # Saturation level: 10 volts
    n_bins=1024,                  # Number of discretization bins: 1024
    responsitivity=1              # Responsitivity: 1
)

# Step 6: Create a FlowCytometer instance
# ---------------------------------------
# The flow cytometer is configured with the source, scatterer distribution, and detectors.
# The 'mie' coupling mechanism models how the particles interact with the laser beam.
cytometer = FlowCytometer(
    source=source,                # Laser source
    scatterer_distribution=scatterer_distribution,  # Particle size distribution
    detectors=[detector_fsc, detector_ssc],  # Detectors: FSC and SSC
    coupling_mechanism='mie'      # Scattering model: Mie
)

# Step 7: Simulate flow cytometer signals
# ---------------------------------------
# Simulate the signals for both detectors (FSC and SSC) as particles pass through the laser beam.
cytometer.simulate_pulse()

# Step 8: Display the properties of the simulation
# ------------------------------------------------
# Print the properties of the simulation setup to better understand flow speed, particle density, and source power.
cytometer.print_properties()

# Step 9: Visualize the generated signals
# ---------------------------------------
# Plot the simulated signals for both FSC and SSC detectors.
cytometer.plot()

# #############################################################################
# The above plot shows the raw simulated signals for Forward Scatter (FSC) and
# Side Scatter (SSC) channels. These signals provide insights into particle size
# and complexity and can be further analyzed for feature extraction, such as peak height and width.
