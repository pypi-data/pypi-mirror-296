# pyposolver/maths/root_finding.py


def bisection_method(func, a, b, tol=1e-6, max_iter=1000):
  """
    Finds a root of a function using the bisection method.

    Parameters:
    - func: The function for which to find a root.
    - a, b: The interval [a, b] in which to search for the root.
    - tol: The tolerance for the root approximation.
    - max_iter: The maximum number of iterations.

    Returns:
    - The approximate root of the function within the specified tolerance.
    """
  if func(a) * func(b) > 0:
    raise ValueError(
        "The function must have opposite signs at the endpoints of the interval."
    )

  iter_count = 0
  while (b - a) / 2 > tol and iter_count < max_iter:
    c = (a + b) / 2
    if func(c) == 0:
      return c
    elif func(c) * func(a) < 0:
      b = c
    else:
      a = c
    iter_count += 1

  return (a + b) / 2


def newton_raphson_method(func, dfunc, x0, tol=1e-6, max_iter=1000):
  """
    Finds a root of a function using the Newton-Raphson method.

    Parameters:
    - func: The function for which to find a root.
    - dfunc: The derivative of the function.
    - x0: The initial guess for the root.
    - tol: The tolerance for the root approximation.
    - max_iter: The maximum number of iterations.

    Returns:
    - The approximate root of the function within the specified tolerance.
    """
  x = x0
  iter_count = 0
  while abs(func(x)) > tol and iter_count < max_iter:
    x -= func(x) / dfunc(x)
    iter_count += 1

  return x
