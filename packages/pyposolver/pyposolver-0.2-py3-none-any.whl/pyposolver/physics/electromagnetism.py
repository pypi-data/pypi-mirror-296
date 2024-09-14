# pyposolver/physics/electromagnetism.py


def electric_field_strength(charge, distance):
  """
    Calculates the electric field strength due to a point charge.

    Parameters:
    - charge: Charge of the point charge (Coulombs).
    - distance: Distance from the point charge (meters).

    Returns:
    - The electric field strength (N/C).
    """
  k = 8.9875517923e9  # Coulomb's constant (N*m^2/C^2)
  return k * charge / distance**2


def magnetic_field_strength(current, distance):
  """
    Calculates the magnetic field strength due to a current-carrying wire.

    Parameters:
    - current: Current flowing through the wire (Amperes).
    - distance: Distance from the wire (meters).

    Returns:
    - The magnetic field strength (Tesla).
    """
  mu_0 = 4e-7 * np.pi  # Vacuum permeability (T*m/A)
  return mu_0 * current / (2 * np.pi * distance)
