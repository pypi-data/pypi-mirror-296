# tests/test_physics.py
import pytest
from pyposolver.physics.mechanics import velocity, force
from pyposolver.physics.electromagnetism import electric_field_strength
from pyposolver.physics.quantum_mechanics import wave_function
from pyposolver.physics.thermodynamics import ideal_gas_law
from pyposolver.physics.fluid_dynamics import bernoullis_equation


# Test cases for mechanics module
def test_velocity():
  # Test case for velocity calculation
  assert velocity(5, 2, 3) == 11


def test_force():
  # Test case for force calculation
  assert force(10, 5) == 50


# Test cases for electromagnetism module
def test_electric_field_strength():
  # Test case for electric field strength calculation
  assert electric_field_strength(2e-6, 0.1) == 1.796e5


# Test cases for quantum mechanics module
def test_wave_function():
  # Test case for wave function calculation
  assert wave_function(0.25) == 0.5


# Test cases for thermodynamics module
def test_ideal_gas_law():
  # Test case for ideal gas law calculation
  assert pytest.approx(ideal_gas_law(100000, 0.1, 300), 0.001) == 0.0405


# Test cases for fluid dynamics module
def test_bernoullis_equation():
  # Test case for Bernoulli's equation
  assert bernoullis_equation(1000, 1.2, 10) == 61600


# Additional test cases for other functions in the physics module
