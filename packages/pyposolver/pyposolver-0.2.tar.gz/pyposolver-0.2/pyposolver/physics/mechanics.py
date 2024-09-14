# pyposolver/physics/mechanics.py


def velocity(initial_velocity, acceleration, time):
  """
    Calculates the final velocity using the kinematic equation:
    v = u + at

    Parameters:
    - initial_velocity: Initial velocity (m/s).
    - acceleration: Acceleration (m/s^2).
    - time: Time duration (s).

    Returns:
    - The final velocity (m/s).
    """
  return initial_velocity + acceleration * time


def displacement(initial_velocity, acceleration, time):
  """
    Calculates the displacement using the kinematic equation:
    s = ut + (1/2)at^2

    Parameters:
    - initial_velocity: Initial velocity (m/s).
    - acceleration: Acceleration (m/s^2).
    - time: Time duration (s).

    Returns:
    - The displacement (m).
    """
  return initial_velocity * time + 0.5 * acceleration * time**2


def force(mass, acceleration):
  """
    Calculates the force using Newton's second law:
    F = ma

    Parameters:
    - mass: Mass (kg).
    - acceleration: Acceleration (m/s^2).

    Returns:
    - The force (N).
    """
  return mass * acceleration


def momentum(mass, velocity):
  """
    Calculates the momentum of an object.

    Parameters:
    - mass: Mass of the object (kg).
    - velocity: Velocity of the object (m/s).

    Returns:
    - The momentum of the object (kg*m/s).
    """
  return mass * velocity


def kinetic_energy(mass, velocity):
  """
    Calculates the kinetic energy of an object.

    Parameters:
    - mass: Mass of the object (kg).
    - velocity: Velocity of the object (m/s).

    Returns:
    - The kinetic energy of the object (Joules).
    """
  return 0.5 * mass * velocity**2


def gravitational_potential_energy(mass,
                                   height,
                                   gravitational_acceleration=9.81):
  """
    Calculates the gravitational potential energy of an object.

    Parameters:
    - mass: Mass of the object (kg).
    - height: Height above the reference point (m).
    - gravitational_acceleration: Acceleration due to gravity (m/s^2), default is Earth's gravity.

    Returns:
    - The gravitational potential energy of the object (Joules).
    """
  return mass * gravitational_acceleration * height
