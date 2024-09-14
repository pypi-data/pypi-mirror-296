# tests/test_physics.py
import pytest
from pyposolver.physics.mechanics import velocity, force

# Test cases for mechanics module
def test_velocity():
  # Test case for velocity calculation
  assert velocity(5, 2, 3) == 11


def test_force():
  # Test case for force calculation
  assert force(10, 5) == 50
