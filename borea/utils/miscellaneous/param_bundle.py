"""
Module math for bundle parameter.
"""
import numpy as np
from borea.datastruct.shot import Shot


def set_param_bundle_diff(shot: Shot, coor_eucli: np.ndarray) -> tuple:
    """
    Setting up the A vector, U vector and V matrix parameters for the differential function
    of beam parameters, in the Euclidean reference frame.
    A = M - S
    U = R @ A
    U = [u1, u2, u3]
    V = [[u3, 0,-u1][ 0,u3,-u2]]
    M euclidean point, S euclidean position shot, R rotation matrix euclidean to image.

    Args:
        shot (Shot): The shot in which we work.
        coor_eucli (np.array): Euclidean coordinates of the point.

    Returns:
        tuple: vector A, vector U and matrix V.
    """
    vect_a = np.vstack([coor_eucli[0] - shot.pos_shot_eucli[0],
                        coor_eucli[1] - shot.pos_shot_eucli[1],
                        coor_eucli[2] - shot.pos_shot_eucli[2]])  # vect_a = M-S
    vect_u = shot.mat_rot_eucli @ vect_a  # U = RA

    mat_v = np.zeros((2 * len(vect_u[0]), 3))
    mat_v[::2, 0] = vect_u[2]
    mat_v[::2, 2] = -vect_u[0]
    mat_v[1::2, 1] = vect_u[2]
    mat_v[1::2, 2] = -vect_u[1]

    return vect_a, vect_u, mat_v
