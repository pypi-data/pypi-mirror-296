# pyposolver/maths/linear_algebra.py


def dot_product(vector1, vector2):
  """
    Computes the dot product of two vectors.

    Parameters:
    - vector1: The first vector.
    - vector2: The second vector.

    Returns:
    - The dot product of the two vectors.
    """
  if len(vector1) != len(vector2):
    raise ValueError("Vectors must have the same length.")
  return sum(v1 * v2 for v1, v2 in zip(vector1, vector2))


def cross_product(vector1, vector2):
  """
    Computes the cross product of two vectors.

    Parameters:
    - vector1: The first vector (3D).
    - vector2: The second vector (3D).

    Returns:
    - The cross product of the two vectors.
    """
  if len(vector1) != 3 or len(vector2) != 3:
    raise ValueError("Vectors must be 3D.")
  return [
      vector1[1] * vector2[2] - vector1[2] * vector2[1],
      vector1[2] * vector2[0] - vector1[0] * vector2[2],
      vector1[0] * vector2[1] - vector1[1] * vector2[0]
  ]


def matrix_multiply(matrix1, matrix2):
  """
    Computes the matrix multiplication of two matrices.

    Parameters:
    - matrix1: The first matrix.
    - matrix2: The second matrix.

    Returns:
    - The result of the matrix multiplication.
    """
  if len(matrix1[0]) != len(matrix2):
    raise ValueError(
        "Number of columns in matrix1 must be equal to number of rows in matrix2."
    )
  result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
  for i in range(len(matrix1)):
    for j in range(len(matrix2[0])):
      for k in range(len(matrix2)):
        result[i][j] += matrix1[i][k] * matrix2[k][j]
  return result
