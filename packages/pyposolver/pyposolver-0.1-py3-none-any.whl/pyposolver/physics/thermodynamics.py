# pyposolver/physics/thermodynamics.py


def ideal_gas_law(pressure, volume, temperature):
  """
    Calculates the number of moles of an ideal gas using the ideal gas law.

    Parameters:
    - pressure: Pressure of the gas (Pascal).
    - volume: Volume of the gas (cubic meter).
    - temperature: Temperature of the gas (Kelvin).

    Returns:
    - The number of moles of the gas.
    """
  R = 8.314  # Ideal gas constant (J/(mol*K))
  return (pressure * volume) / (R * temperature)


def heat_transfer_conduction(area, thermal_conductivity,
                             temperature_difference, thickness):
  """
    Calculates the rate of heat transfer by conduction through a material.

    Parameters:
    - area: Cross-sectional area of the material (square meter).
    - thermal_conductivity: Thermal conductivity of the material (W/(m*K)).
    - temperature_difference: Temperature difference across the material (Kelvin).
    - thickness: Thickness of the material (meter).

    Returns:
    - The rate of heat transfer by conduction (Watt).
    """
  return (thermal_conductivity * area * temperature_difference) / thickness
