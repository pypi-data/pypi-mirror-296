# pyposolver/maths/integration.py

def trapezoidal_rule(f, a, b, n=100):
    """
    Approximates the integral of f(x) from a to b using the trapezoidal rule with n subintervals.
    """
    h = (b - a) / n
    total = (f(a) + f(b)) / 2.0
    for i in range(1, n):
        total += f(a + i * h)
    return total * h
