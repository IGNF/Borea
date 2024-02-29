"""
A script combining various data conversion and format verification functions.
"""
from typing import Union
import numpy as np


def check_array_transfo(x: Union[np.ndarray, float],
                        y: Union[np.ndarray, float],
                        z: Union[np.ndarray, float] = None) -> tuple:
    """
    Checks the dimension of vectors if dim = 1 outputs the element in a variable.
    x,y,z are in the same dimension and they must be vectors if array
    possible dimension if array : (1,), (n,), (n,1) or (1,n).

    Args:
        x (Union[np.array, float]): Vector x.
        y (Union[np.array, float]): Vector y.
        z (Union[np.array, float]): Vector z.

    Returns:
        tuple: x, y, z.
    """
    if isinstance(x, np.ndarray):  # look if is an array
        t = np.shape(x)
        if len(t) == 1:  # look dim == (n,)
            if t[0] == 1:  # look n == 1
                # takes out the elements
                x = float(x[0])
                y = float(y[0])
                if z is not None:
                    z = float(z[0])

        if len(t) == 2:  # look dim == (n,m)
            if t[0] != 1:  # look n != 1
                # conversion dim (n,1) to (1,n)
                x = x.T
                y = y.T
                if z is not None:
                    z = z.T
            # conversion dim (1,n) to (n,)
            x = np.squeeze(x, axis=0)
            y = np.squeeze(y, axis=0)
            if z is not None:
                z = np.squeeze(z, axis=0)

            # same checkup to the top
            t2 = np.shape(x)
            if len(t2) == 1:
                if t2[0] == 1:
                    x = float(x[0])
                    y = float(y[0])
                    if z is not None:
                        z = float(z[0])

    return x, y, z
