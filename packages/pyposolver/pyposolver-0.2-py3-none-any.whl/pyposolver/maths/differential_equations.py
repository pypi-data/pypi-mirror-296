# pyposolver/maths/differential_equations.py


def euler_method(dy_dx, initial_condition, x_values):
  """
    Solves a first-order ordinary differential equation using Euler's method.

    Parameters:
    - dy_dx: A function representing the derivative dy/dx.
    - initial_condition: The initial condition y(x0) = y0.
    - x_values: A list of x values at which to evaluate the solution.

    Returns:
    - A list of corresponding y values approximating the solution.
    """
  x0, y0 = initial_condition
  y_values = [y0]
  for x in x_values[1:]:
    y_next = y_values[-1] + dy_dx(x, y_values[-1]) * (x - x_values[-2])
    y_values.append(y_next)
  return y_values


def runge_kutta_method(dy_dx, initial_condition, x_values):
  """
    Solves a first-order ordinary differential equation using the Runge-Kutta method (4th order).

    Parameters:
    - dy_dx: A function representing the derivative dy/dx.
    - initial_condition: The initial condition y(x0) = y0.
    - x_values: A list of x values at which to evaluate the solution.

    Returns:
    - A list of corresponding y values approximating the solution.
    """
  x0, y0 = initial_condition
  y_values = [y0]
  for i in range(1, len(x_values)):
    h = x_values[i] - x_values[i - 1]
    k1 = h * dy_dx(x_values[i - 1], y_values[-1])
    k2 = h * dy_dx(x_values[i - 1] + h / 2, y_values[-1] + k1 / 2)
    k3 = h * dy_dx(x_values[i - 1] + h / 2, y_values[-1] + k2 / 2)
    k4 = h * dy_dx(x_values[i - 1] + h, y_values[-1] + k3)
    y_next = y_values[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    y_values.append(y_next)
  return y_values
