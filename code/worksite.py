"""
Worksite data class module
"""
import code.shot as shot
import numpy as np


class Worksite:
    """
    Worksite class
    """
    def __init__(self, name: str) -> None:
        """
        Class definition of Worksite

        :param str name : Name of the worksite.
        :param list shots: Shots list of the worksite, list<Shot>.
        """
        self.name = name
        self.shots = []

    def add_shot(self, name_shot: str, pos_shot: np.array,
                 ori_shot: np.array, name_cam: str) -> None:
        """
        Add Shot to the attribut Shots

        :param str name_shot : Name of the shot.
        :param numpy.array pos_shot : Array of coordinate position [X, Y, Z].
        :param numpy.array ori_shot : Array of orientation of the shot [Omega, Phi, Kappa].
        :param str name_cam : Name of the camera.
        """
        self.shots.append(shot.Shot(name_shot=name_shot,
                                    pos_shot=pos_shot,
                                    ori_shot=ori_shot,
                                    name_cam=name_cam))
