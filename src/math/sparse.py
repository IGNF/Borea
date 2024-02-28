"""
Module math
"""
from scipy.sparse import coo_matrix
import numpy as np


def invert_diag_sparse_matrix_3_3(mat_inv: np.ndarray) -> np.ndarray:
    """
    Block matrix inversion.

    Args:
        mat (np.array): Matrix to flip.

    Returns:
        np.array: Flip matrix.
    """
    mat = np.c_[np.pad(mat_inv.diagonal(-2), (2, 0)),
                np.pad(mat_inv.diagonal(-1), (1, 0)),
                mat_inv.diagonal(0),
                np.pad(mat_inv.diagonal(1), (0, 1)),
                np.pad(mat_inv.diagonal(2), (0, 2))]

    mat[::3, :] = np.roll(mat[::3, :], -2)
    mat[1::3, :] = np.roll(mat[1::3, :], -1)

    data = np.linalg.inv(mat[:, :-2].reshape(1, -1, 3, 3)).flatten()
    coord_i = np.repeat(np.arange(mat_inv.shape[0]), 3)
    coord_j = np.tile(np.arange(mat_inv.shape[0]).reshape(-1, 3), 3).flatten()

    return coo_matrix((data, (coord_i, coord_j)), shape=mat_inv.shape).tocsr()
