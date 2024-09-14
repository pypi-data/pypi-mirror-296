# pyposolver/maths/integration.py


def trapezoidal_rule(func, a, b, n):
  """
    Approximates the definite integral of a function using the trapezoidal rule.

    Parameters:
    - func: The function to integrate.
    - a, b: The interval [a, b] over which to integrate.
    - n: The number of subintervals to use for the approximation.

    Returns:
    - The approximate value of the definite integral.
    """
  h = (b - a) / n
  result = 0.5 * (func(a) + func(b))
  for i in range(1, n):
    result += func(a + i * h)
  result *= h
  return result


def simpsons_rule(func, a, b, n):
  """
    Approximates the definite integral of a function using Simpson's rule.

    Parameters:
    - func: The function to integrate.
    - a, b: The interval [a, b] over which to integrate.
    - n: The number of subintervals to use for the approximation (must be even).

    Returns:
    - The approximate value of the definite integral.
    """
  if n % 2 != 0:
    raise ValueError("Number of subintervals must be even for Simpson's rule.")
  h = (b - a) / n
  result = func(a) + func(b)
  for i in range(1, n, 2):
    result += 4 * func(a + i * h)
  for i in range(2, n - 1, 2):
    result += 2 * func(a + i * h)
  result *= h / 3
  return result


def midpoint_rule(func, a, b, n):
  """
    Approximates the definite integral of a function using the midpoint rule.

    Parameters:
    - func: The function to integrate.
    - a, b: The interval [a, b] over which to integrate.
    - n: The number of subintervals to use for the approximation.

    Returns:
    - The approximate value of the definite integral.
    """
  h = (b - a) / n
  result = 0
  for i in range(n):
    result += func(a + (i + 0.5) * h)
  result *= h
  return result


# Additional utility functions
def integrate(func, a, b, n, method='trapezoidal'):
  """
    Approximates the definite integral of a function using the specified integration method.

    Parameters:
    - func: The function to integrate.
    - a, b: The interval [a, b] over which to integrate.
    - n: The number of subintervals to use for the approximation.
    - method: The integration method to use ('trapezoidal', 'simpsons', or 'midpoint').

    Returns:
    - The approximate value of the definite integral.
    """
  if method == 'trapezoidal':
    return trapezoidal_rule(func, a, b, n)
  elif method == 'simpsons':
    return simpsons_rule(func, a, b, n)
  elif method == 'midpoint':
    return midpoint_rule(func, a, b, n)
  else:
    raise ValueError(
        "Invalid integration method. Supported methods: 'trapezoidal', 'simpsons', 'midpoint'"
    )
