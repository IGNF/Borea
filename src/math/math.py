"""
Function to normalize data.
"""
import numpy as np


def normalize(array: np.ndarray) -> tuple:
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


def dist_2pts(pt1: np.ndarray, pt2: np.ndarray) -> float:
    """
    Calculate the distance of two points.

    Args:
        pt1 (np.array): Coordinates of the first point.
        pt2 (np.array): Coordinates of the second point.

    Returns:
        float: The distance.
    """
    return np.linalg.norm(pt1 - pt2)


def min_max_pt(array: np.ndarray, type_m: str) -> tuple:
    """
    Get min or max of coordinnate 2D in an array of dim (2,n).

    Args:
        array (np.array): Array data to get min or max.
        type_m (str): Type min or max.

    Returns:
        tuple: min or max Coordinate of one point and index in array.
    """
    if type_m == "min":
        func = np.argmin
    else:
        func = np.argmax

    arg_col = func(array[0])
    arg_lin = func(array[1])
    pt_col = array[:, arg_col]
    pt_lin = array[:, arg_lin]

    if (pt_col == pt_lin).all():
        return pt_col, arg_col

    d1 = dist_2pts(np.array([0, 0]), pt_col)
    d2 = dist_2pts(np.array([0, 0]), pt_lin)
    if (d1 <= d2 and type_m == "min") or (d1 >= d2 and type_m == "max"):
        return pt_col, arg_col

    return pt_lin, arg_lin


def angle_degree_2vect(u: np.ndarray, v: np.ndarray) -> float:
    """
    Calculates degree angle between two vectors.

    Args:
        u (np.array): Fisrt vector.
        v (np.array): Second vector.

    Returns:
        float: Degree angle between two vectors.
    """
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    costheta = (u @ v)/(nu * nv)
    return np.arccos(costheta)*180/np.pi
