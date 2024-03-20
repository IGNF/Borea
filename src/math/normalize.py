"""
Function to normalize data.
"""
import numpy as np


def normalize(array):
    """
    Normalize array.

    Args:
        array (np.array): Array data to normalize.

    Returns:
        tuple: data normalize, offset of data and scale of data.
    """
    offset = (np.min(array) + np.max(array))/2
    scale = (np.max(array) - np.min(array))/2
    array_norm = (array - offset) / scale
    return array_norm, offset, scale
