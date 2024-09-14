# pyposolver/maths/root_finding.py

def bisection_method(f, a, b, tol=1e-6, max_iter=100):
    """
    Finds a root of the function f in the interval [a, b] using the bisection method.
    """
    if f(a) * f(b) >= 0:
        raise ValueError("The function must have different signs at the endpoints a and b.")

    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        elif f(c) * f(a) < 0:
            b = c
        else:
            a = c

    raise RuntimeError("Maximum number of iterations reached without convergence.")


def newton_raphson_method(f, df, x0, tol=1e-6, max_iter=100):
    """
    Finds a root of the function f using the Newton-Raphson method starting from x0.
    """
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(fx) < tol:
            return x
        if dfx == 0:
            raise ValueError("The derivative is zero. Newton-Raphson method fails.")
        x = x - fx / dfx

    raise RuntimeError("Maximum number of iterations reached without convergence.")
