import pytest
import numpy as np
from FlowCyPy import ScattererDistribution, Detector, Source, FlowCell
from FlowCyPy import distribution
from FlowCyPy.coupling_mechanism.rayleigh import compute_detected_signal
from FlowCyPy.units import micrometer, refractive_index_unit
from FlowCyPy.units import volt, watt, meter, hertz, particle, milliliter
from FlowCyPy.population import Population

@pytest.fixture
def normal_size_distribution():
    """Fixture for creating a distribution.Normal."""
    return distribution.Normal(
        mean=1.0 * micrometer,
        std_dev=0.1 * micrometer,
    )

@pytest.fixture
def normal_ri_distribution():
    """Fixture for creating a distribution.Normal."""
    return distribution.Normal(
        mean=1.5 * refractive_index_unit,
        std_dev=0.1 * refractive_index_unit,
    )

@pytest.fixture
def normal_population(normal_size_distribution, normal_ri_distribution):
    """Fixture for creating a Population."""
    return Population(
        size=normal_size_distribution,
        refractive_index=normal_ri_distribution,
        concentration=1.8e9 * particle / milliliter,
        name="Default population"
    )

@pytest.fixture
def default_flow_cell():
    return FlowCell(
        flow_speed=80e-6,
        flow_area=1e-6,
        total_time=1.0,
    )

@pytest.fixture
def detector():
    return Detector(
        phi_angle=90,
        NA=0.1,
        name='first detector',
        responsitivity=1.0,          # Responsitivity of the detector
        acquisition_frequency=1e4,   # Sampling frequency: 10,000 Hz
        noise_level=1e-2,            # Signal noise level: 1 millivolts
        baseline_shift=0.01,         # Signal noise level: 0.5 volts
        saturation_level=1e30,       # Signal saturation at 1000 volts
        n_bins=1024                  # Discretization bins: 1024
    )

@pytest.fixture
def scatterer_distribution(normal_population, default_flow_cell):
    return ScattererDistribution(
        populations=[normal_population],
        flow=default_flow_cell,
    )

@pytest.fixture
def source():
    return Source(
        NA=0.2,
        wavelength=1550e-9,    # Wavelength of the laser source: 1550 nm
        optical_power=200e-3,  # Optical power of the laser source: 200 milliwatt
    )

def test_generate_scatterer_size(scatterer_distribution):
    """
    Test if the sizes are generated correctly in the ScattererDistribution.
    """
    sizes = scatterer_distribution.size_list

    assert sizes is not None, "Scatterer sizes should be generated."
    assert len(sizes) > 0, f"Expected 10 scatterer sizes, but got {len(sizes)}."
    assert sizes.magnitude.min() > 0, f"Expected all sizes to be positive, but got a minimum size of {sizes.magnitude.min()}."

def test_rayleigh_mechanism_output(detector, scatterer_distribution, source):
    """
    Test the detected power output of the Rayleigh scattering mechanism.
    """
    detected_power = compute_detected_signal(
        source=source,
        detector=detector,
        scatterer_distribution=scatterer_distribution
    )

    assert detected_power is not None, "Detected power should not be None."
    assert np.all(detected_power > 0), f"Expected detected power to be positive, but got {detected_power}."

def test_detector_properties(detector):
    """
    Test the detector's properties and ensure they are correctly initialized.
    """
    assert detector.NA == 0.1, f"Expected detector numerical aperture to be 0.1, but got {detector.NA}."
    assert detector.responsitivity == 1.0 * volt / watt, f"Expected detector responsitivity to be 1.0, but got {detector.responsitivity}."
    assert detector.acquisition_frequency == 1e4 * hertz, f"Expected acquisition frequency to be 10,000 Hz, but got {detector.acquisition_frequency}."
    assert detector.noise_level == 1e-2 * volt, f"Expected noise level to be 0.01, but got {detector.noise_level}."
    assert detector.saturation_level == 1e30 * volt, f"Expected saturation level to be 1e30, but got {detector.saturation_level}."
    assert detector.n_bins == 1024, f"Expected 1024 bins, but got {detector.n_bins}."

def test_source_properties(source):
    """
    Test the properties of the light source to ensure they are correctly set.
    """
    assert source.NA == 0.2, f"Expected source numerical aperture to be 0.2, but got {source.NA}."
    assert source.wavelength == 1550e-9 * meter, f"Expected source wavelength to be 1550 nm (1.55e-6 m), but got {source.wavelength}."
    assert source.optical_power == 200e-3 * watt, f"Expected source optical power to be 200 mW, but got {source.optical_power}."

if __name__ == '__main__':
    pytest.main([__file__])
