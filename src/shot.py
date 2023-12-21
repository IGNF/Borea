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

        :param str name_shot : Name of the shot.
        :param numpy.array pos_shot : Array of coordinate position [X, Y, Z].
        :param numpy.array ori_shot : Array of orientation of the shot [Omega, Phi, Kappa].
        :param str name_cam : Name of the camera.
        """
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.ori_shot = ori_shot
        self.name_cam = name_cam
