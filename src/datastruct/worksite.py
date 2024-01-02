"""
Worksite data class module
"""
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera


class Worksite:
    """
    Worksite class
    """
    def __init__(self, name: str) -> None:
        """
        Class definition of Worksite

        Args:
            name (str): Name of the worksite.
        """
        self.name = name
        self.shots = {}
        self.cameras = {}

    def add_shot(self, name_shot: str, pos_shot: np.array,
                 ori_shot: np.array, name_cam: str) -> None:
        """
        Add Shot to the attribut Shots

        Args:
            name_shot (str): Name of the shot.
            pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
            ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa].
            name_cam (str): Name of the camera.
        """
        self.shots[name_shot] = Shot(name_shot=name_shot,
                                     pos_shot=pos_shot,
                                     ori_shot=ori_shot,
                                     name_cam=name_cam)

    def add_camera(self, name_camera: str, ppax: float,
                   ppay: float, focal: float) -> None:
        """
        Add data camera in the Worksite

        Args:
            name_camera (str): Name of the camera.
            ppax (float): Center of distortion in x.
            ppay (float): Center of distortion in y.
            focal (float): Focal of the camera.
        """
        self.cameras[name_camera] = Camera(name_camera=name_camera,
                                           ppax=ppax,
                                           ppay=ppay,
                                           focal=focal)
