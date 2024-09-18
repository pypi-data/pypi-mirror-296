import numpy as np
import pytest
from FlowCyPy import Analyzer
from FlowCyPy.units import second, volt, hertz, watt, degree, micrometer, meter, particle, milliliter, refractive_index_unit, millisecond
from FlowCyPy import distribution
from FlowCyPy.population import Population
from FlowCyPy.utils import generate_gaussian_signal
from FlowCyPy import FlowCytometer, Detector, Scatterer, Source, FlowCell
from unittest.mock import patch
from FlowCyPy import peak_finder
import matplotlib.pyplot as plt
np.random.seed(10)

@pytest.fixture
def flow_cell():
    return FlowCell(
        flow_speed=0.2 * meter / second,
        flow_area=1e-6 * meter * meter,
        total_time=1e-3 * second,
    )


@pytest.fixture
def default_size_distribution():
    return distribution.Normal(
        mean=1.0 * micrometer,
        std_dev=0.1 * micrometer
    )

@pytest.fixture
def default_ri_distribution():
    return distribution.Normal(
        mean=1.0 * refractive_index_unit,
        std_dev=0.1 * refractive_index_unit
    )

@pytest.fixture
def default_population(default_size_distribution, default_ri_distribution):
    return Population(
        size=default_size_distribution,
        refractive_index=default_ri_distribution,
        concentration=1.8e5 * particle / milliliter,
        name="Default population"
    )


@pytest.fixture
def default_scatterer(flow_cell, default_population):
    return  Scatterer(
        flow_cell=flow_cell,
        populations=[default_population]
    )


@pytest.fixture
def default_source():
    return Source(
        numerical_aperture=1,
        wavelength=1550e-9 * meter,
        optical_power=1e-3 * watt,
    )

@pytest.fixture
def default_front_detector():
    return Detector(
        name='default_0',
        numerical_aperture=1,
        phi_angle=0 * degree,
        responsitivity=1 * volt / watt,
        sampling_freq=1e5 * hertz,
        noise_level=0 * volt,
        saturation_level=1 * volt,
        baseline_shift=0.0 * volt,
        n_bins='12bit',
    )

@pytest.fixture
def default_side_detector():
    return Detector(
        name='default_1',
        numerical_aperture=1,
        phi_angle=0 * degree,
        responsitivity=1 * volt / watt,
        sampling_freq=1e5 * hertz,
        noise_level=0 * volt,
        saturation_level=1 * volt,
        baseline_shift=0.0 * volt,
        n_bins='12bit',
    )

@pytest.fixture
def default_cytometer(default_source, default_front_detector, default_side_detector, default_scatterer):
    """Test the simulation of flow cytometer signals."""
    cytometer = FlowCytometer(
        source=default_source,
        detectors=[default_front_detector, default_side_detector],
        scatterer=default_scatterer,
        coupling_mechanism='mie'
    )
    cytometer.simulate_pulse()

    return cytometer

algorithm = peak_finder.MovingAverage(
    threshold=0.001 * volt,
    window_size=0.8 * second,
    # min_peak_distance=1e-1 * second
)

def test_pulse_analyzer_peak_detection(default_cytometer):
    """Test peak detection in the pulse analyzer."""
    # Create a synthetic signal with two Gaussian peaks
    time = np.linspace(0, 10, 1000) * second

    detector_0 = generate_gaussian_signal(
        time=time,
        centers=[3, 7, 8],
        heights=[1, 1, 4],
        stds=[0.1, 0.1, 1]
    )

    detector_1 = generate_gaussian_signal(
        time=time,
        centers=[3.05, 7, 5],
        heights=[1, 2, 4],
        stds=[0.1, 0.1, 1]
    )

    default_cytometer.detectors = [detector_0, detector_1]

    # Initialize Analyzer with time and signal
    analyzer = Analyzer(default_cytometer, algorithm=algorithm)

    analyzer.run_analysis()

    analyzer.get_coincidence(margin=0.1 * second)

    # Check that two peaks were detected
    assert len(analyzer.coincidence[detector_0.name]) == 2,\
        "Number of detected peaks is not correct."

    # # Check that the peaks are located near the expected positions
    expected_peak_positions = [3, 7] * second  # Expected positions in the time array

    assert np.all(np.isclose(analyzer.coincidence[detector_0.name]['PeakTimes'], expected_peak_positions, atol=0.1 * second)),\
        f"Peak location [{analyzer.coincidence[detector_0.name]['PeakTimes']}] are incorrect. Supposed to be: [{expected_peak_positions}]"

@patch('matplotlib.pyplot.show')
def test_pulse_analyzer_width_and_area(mock_show, default_cytometer):
    """Test width and area calculation in the pulse analyzer."""
    # Create a synthetic signal with one Gaussian peak
    n_peaks = 4
    centers = np.linspace(1, 8, n_peaks)
    heights = np.random.rand(n_peaks)
    stds = np.random.rand(n_peaks) * 0.1

    time = np.linspace(0, 10, 1000) * second

    detector_0 = generate_gaussian_signal(
        time=time,
        centers=centers,
        heights=heights * np.random.rand(n_peaks) / 4,
        stds=stds
    )

    detector_1 = generate_gaussian_signal(
        time=time,
        centers=centers,
        heights=heights,
        stds=stds
    )

    default_cytometer.detectors = [detector_0, detector_1]

    # Initialize Analyzer with time and signal
    analyzer = Analyzer(default_cytometer, algorithm=algorithm)

    analyzer.run_analysis(compute_peak_area=True)

    analyzer.get_coincidence(margin=0.001 * millisecond)

    analyzer.display_features()

    analyzer.plot_peak()

    plt.close()

    algorithm.plot(detector_1)

    plt.close()

    analyzer.plot()

    plt.close()

    analyzer.generate_report(filename='test_report')

    # Check that the width is close to the expected value (based on the standard deviation of the Gaussian)
    expected_widths = 2 * np.sqrt(2 * np.log(2)) * stds * second  # Full width at half maximum (FWHM)
    measured_widths = analyzer.coincidence[detector_0.name].Widths.values

    assert np.allclose(measured_widths.numpy_data, expected_widths.magnitude, atol=0.5 * 10), (
        f"Measured width: [{measured_widths.numpy_data}] does not match expected value: [{expected_widths}]."
    )

    # Check that the area is close to the expected value (integral of the Gaussian)
    expected_area = np.sqrt(2 * np.pi) * stds * second * volt  # Area under the Gaussian curve
    measured_area = analyzer.coincidence[detector_0.name].Areas.values

    assert np.allclose(measured_area.numpy_data, expected_area.magnitude, atol=0.5 * 100),\
        f"Measured area: [{measured_area.numpy_data}] does not match expected value: [{expected_area.magnitude}]."

if __name__ == '__main__':
    pytest.main([__file__])
