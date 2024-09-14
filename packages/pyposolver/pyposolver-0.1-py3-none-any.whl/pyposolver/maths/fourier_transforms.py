# pyposolver/maths/fourier_transforms.py

import numpy as np


def discrete_fourier_transform(signal):
  """
    Computes the discrete Fourier transform (DFT) of a signal.

    Parameters:
    - signal: The input signal (time-domain).

    Returns:
    - The complex-valued DFT coefficients.
    """
  N = len(signal)
  n = np.arange(N)
  k = n.reshape((N, 1))
  exp_term = np.exp(-2j * np.pi * k * n / N)
  return np.dot(exp_term, signal)


def inverse_discrete_fourier_transform(frequencies):
  """
    Computes the inverse discrete Fourier transform (IDFT) to reconstruct the original signal.

    Parameters:
    - frequencies: The complex-valued DFT coefficients.

    Returns:
    - The reconstructed signal (time-domain).
    """
  N = len(frequencies)
  n = np.arange(N)
  k = n.reshape((N, 1))
  exp_term = np.exp(2j * np.pi * k * n / N)
  return np.dot(exp_term, frequencies) / N
