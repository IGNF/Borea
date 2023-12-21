"""
Acquisition data class module
"""
import numpy as np


class Shot:
    """
    Acquisition data class
    """
    def __init__(self, name_shot: str,
                 pos_shot: np.array, ori_shot: np.array, name_cam: str) -> None:
        """
        Shot class definition

        Args:
            name_shot (str): Name of the shot.
            pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
            ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa].
            name_cam (str): Name of the camera.
        """
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.ori_shot = ori_shot
        self.name_cam = name_cam
