# pyposolver/physics/quantum_mechanics.py


def wave_function(probability_density):
  """
    Calculates the wave function from the probability density function.

    Parameters:
    - probability_density: The probability density function.

    Returns:
    - The wave function.
    """
  return np.sqrt(probability_density)


def schroedinger_equation(potential_energy, wave_function):
  """
    Solves the time-independent Schroedinger equation for a given potential energy.

    Parameters:
    - potential_energy: The potential energy function.
    - wave_function: The wave function.

    Returns:
    - The solution to the Schroedinger equation.
    """
  return potential_energy * wave_function
