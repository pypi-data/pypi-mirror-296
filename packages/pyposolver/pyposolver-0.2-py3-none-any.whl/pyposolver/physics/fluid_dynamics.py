# pyposolver/physics/fluid_dynamics.py


def bernoullis_equation(pressure, density, velocity):
  """
    Calculates the total mechanical energy per unit mass of a fluid using Bernoulli's equation.

    Parameters:
    - pressure: Pressure of the fluid (Pascal).
    - density: Density of the fluid (kg/m^3).
    - velocity: Velocity of the fluid (m/s).

    Returns:
    - The total mechanical energy per unit mass of the fluid (J/kg).
    """
  return pressure + 0.5 * density * velocity**2


def reynolds_number(density, velocity, length, viscosity):
  """
    Calculates the Reynolds number for a fluid flow.

    Parameters:
    - density: Density of the fluid (kg/m^3).
    - velocity: Velocity of the fluid (m/s).
    - length: Characteristic length of the flow (meter).
    - viscosity: Dynamic viscosity of the fluid (Pa*s).

    Returns:
    - The Reynolds number.
    """
  return (density * velocity * length) / viscosity
