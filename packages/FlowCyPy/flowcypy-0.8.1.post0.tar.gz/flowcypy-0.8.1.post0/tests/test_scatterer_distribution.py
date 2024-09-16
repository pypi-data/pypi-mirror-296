import pytest
from unittest.mock import patch
import matplotlib.pyplot as plt
import numpy as np
from FlowCyPy.scatterer import Scatterer
from FlowCyPy import distribution as dist
from FlowCyPy.flow_cell import FlowCell
from FlowCyPy.units import micrometer, refractive_index_unit, nanometer, milliliter, particle
from FlowCyPy.population import Population


default_concentration = 1.8e7 * particle / milliliter

# Fixtures to set up a default Flow and Distributions
@pytest.fixture
def default_flow():
    """Fixture for creating a default Flow object."""
    return FlowCell(
        flow_speed=80e-6,
        flow_area=1e-6,
        total_time=1.0,
    )

# Parametrize different distributions
distributions = [
    dist.Normal(mean=1.0 * micrometer, std_dev=1.0 * nanometer),
    dist.LogNormal(mean=1.0 * micrometer, std_dev=0.01 * micrometer),
    dist.Uniform(lower_bound=0.5 * micrometer, upper_bound=1.5 * micrometer),
]

@pytest.mark.parametrize("distribution", distributions, ids=lambda x: x.__class__)
def test_generate_distribution_size(distribution, default_flow):
    """Test if the Scatterer generates sizes correctly for each distribution type."""
    # Get the distribution from the fixtures

    ri_distribution = dist.Normal(
        mean=1.4 * refractive_index_unit,
        std_dev=0.01 * refractive_index_unit
    )

    population_0 = Population(
        size=distribution,
        refractive_index=ri_distribution,
        concentration=default_concentration,
        name="Default population"
    )

    # Create the Scatt
    # ererDistribution object with the chosen distribution
    scatterer_distribution = Scatterer(
        flow=default_flow,
        populations=[population_0]
    )

    print('scatterer_distribution', scatterer_distribution.size_list)

    # Check that sizes were generated and are positive
    assert scatterer_distribution.size_list.size > 0, "Generated size array is empty."
    assert np.all(scatterer_distribution.size_list.magnitude > 0), "Some generated sizes are not positive."

    # Check if the sizes follow the expected bounds depending on the distribution type
    if isinstance(distribution, dist.Normal):
        expected_mean = distribution.mean

        generated_mean = np.mean(scatterer_distribution.size_list)

        assert np.isclose(generated_mean, expected_mean, rtol=1e-1), (
            f"Normal distribution: Expected mean {expected_mean}, but got {generated_mean}"
        )

    elif isinstance(distribution, dist.LogNormal):
        assert np.all(scatterer_distribution.size_list.magnitude > 0), "Lognormal distribution generated non-positive sizes."

    elif isinstance(distribution, dist.Uniform):
        lower_bound = distribution.lower_bound
        upper_bound = distribution.upper_bound

        assert np.all((scatterer_distribution.size_list >= lower_bound) & (scatterer_distribution.size_list <= upper_bound)), (
            f"Uniform distribution: Sizes are out of bounds [{lower_bound}, {upper_bound}]"
        )

    elif isinstance(distribution, dist.Delta):
        singular_value = distribution.size_value

        assert np.all(scatterer_distribution.size_list == singular_value), (
            f"Singular distribution: All sizes should be {singular_value}, but got varying sizes."
        )


@pytest.mark.parametrize("distribution", distributions, ids=lambda x: x.__class__)
def test_generate_longitudinal_positions(default_flow, distribution):
    """Test the generation of longitudinal positions based on Poisson process."""
    ri_distribution = dist.Normal(
        mean=1.4 * refractive_index_unit,
        std_dev=0.01 * refractive_index_unit
    )

    population_0 = Population(
        size=distribution,
        refractive_index=ri_distribution,
        concentration=default_concentration,
        name="Default population"
    )

    scatterer_distribution = Scatterer(
        flow=default_flow,
        populations=[population_0]
    )

    # Assert correct shape of generated longitudinal positions
    for population in scatterer_distribution.populations:
        assert population.longitudinal_positions.size > 0, "Generated longitudinal positions array has incorrect shape."

    # Assert that longitudinal positions are increasing (since they are cumulative)
    for population in scatterer_distribution.populations:
        assert np.all(np.diff(population.longitudinal_positions.magnitude) >= 0), "Longitudinal positions are not monotonically increasing."

    # Assert that no positions are negative
    for population in scatterer_distribution.populations:
        assert np.all(population.longitudinal_positions.magnitude >= 0), "Some longitudinal positions are negative."


@patch('matplotlib.pyplot.show')
@pytest.mark.parametrize("distribution", distributions, ids=lambda x: x.__class__)
def test_plot_positions(mock_show, default_flow, distribution):
    """Test the plotting of longitudinal positions."""
    ri_distribution = dist.Normal(
        mean=1.4 * refractive_index_unit,
        std_dev=0.01 * refractive_index_unit
    )

    population_0 = Population(
        size=distribution,
        refractive_index=ri_distribution,
        concentration=default_concentration,
        name="Default population"
    )

    scatterer_distribution = Scatterer(
        flow=default_flow,
        populations=[population_0]
    )

    scatterer_distribution.plot()

    plt.close()


if __name__ == '__main__':
    pytest.main([__file__])
