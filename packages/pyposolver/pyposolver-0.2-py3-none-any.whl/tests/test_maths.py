# tests/test_maths.py
import pytest
from pyposolver.maths.integration import trapezoidal_rule
from pyposolver.maths.root_finding import bisection_method, newton_raphson_method
from pyposolver.maths.linear_algebra import dot_product, cross_product, matrix_multiply

# Test cases for integration functions
def test_trapezoidal_rule():
    # Define a test function
    def f(x):
        return x**2

    # Test integration of f(x) = x^2 from 0 to 1
    assert pytest.approx(trapezoidal_rule(f, 0, 1), 0.001) == 1/3

# Test cases for root-finding functions
def test_bisection_method():
    # Define a test function
    def f(x):
        return x**2 - 4

    # Test root-finding of f(x) = x^2 - 4 in the interval [0, 3]
    assert pytest.approx(bisection_method(f, 0, 3), 0.001) == 2

def test_newton_raphson_method():
    # Define a test function and its derivative
    def f(x):
        return x**3 - 2*x - 5

    def df(x):
        return 3*x**2 - 2

    # Test root-finding of f(x) = x^3 - 2x - 5 with an initial guess of 2
    assert pytest.approx(newton_raphson_method(f, df, 2), 0.001) == 2.094

# Test cases for linear algebra functions
def test_dot_product():
    # Define two vectors
    vector1 = [1, 2, 3]
    vector2 = [4, 5, 6]

    # Test dot product of the two vectors
    assert dot_product(vector1, vector2) == 32

def test_cross_product():
    # Define two 3D vectors
    vector1 = [1, 2, 3]
    vector2 = [4, 5, 6]

    # Test cross product of the two vectors
    assert cross_product(vector1, vector2) == [-3, 6, -3]

def test_matrix_multiply():
    # Define two matrices
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]

    # Test matrix multiplication of the two matrices
    assert matrix_multiply(matrix1, matrix2) == [[19, 22], [43, 50]]

# Additional test cases for other functions in the maths module
