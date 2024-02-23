"""
A script combining various data conversion and format verification functions.
"""
from typing import Union
import numpy as np


def change_dim(x: np.ndarray, dim: tuple) -> Union[np.ndarray, float]:
    """
    Change dimension of x to the dim given.

    Args:
        x (np.array): Values to change dim.
        dim (tuble): The dimension to have.

    Returns:
        Union[np.array, float]: x with the new dimension.
    """
    if np.shape(x) != dim:
        x = x.reshape(dim)

    return x
