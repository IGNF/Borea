"""
Acquisition data class module
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class Shot:
    """
    Shot class definition

    Args:
        name_shot (str): Name of the shot.
        pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
        ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa].
        name_cam (str): Name of the camera.
    """
    name_shot : str
    pos_shot : np.array
    ori_shot : np.array
    name_cam : str
