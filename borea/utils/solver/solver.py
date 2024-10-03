"""
Least square solver used by Borea
"""
import numpy as np


def npsolve(mat_a: np.ndarray, mat_b: np.ndarray) -> np.ndarray:
    """
    Solver used by Borea to resolve Ax = B

    Args:
        mat_a (np.ndarray): Matrix A
        mat_b (np.ndarray): Matrix B

    Returns:
        np.ndarray: the result x
    """
    return np.linalg.lstsq(mat_a, mat_b, rcond=None)[0]
