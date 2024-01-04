"""
Worksite data class module
"""
import sys
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.gcp import GCP


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
        self.copoints = {}
        self.gcp = {}

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

    def add_copoint(self, name_point: str, name_shot: str, x: float, y: float) -> None:
        """
        Add linking point between acquisition in two part
        One in self.copoints a dict with name_point the key and list of acquisition the result
        And One in self.shot[name_shot].copoints a dict whit
        name_point the key and list of coordinate x (column) y (line) the result in list

        Agrs:
            name_point (str): Name of the connecting point
            name_shot (str): Name of the acquisition
            x (float): pixel position of the point in column
            y (float): pixel position of the point in line
        """
        if name_shot not in self.shots:
            print(f"The shot {name_shot} doesn't exist in list of shots")
            sys.exit()

        if name_point not in self.copoints:
            self.copoints[name_point] = []

        if name_point not in self.shots[name_shot].copoints:
            self.shots[name_shot].copoints[name_point] = [x, y]
        else:
            print("\n :--------------------------:")
            print("Warning : connecting point duplicate")
            print(f"The point {name_point} already exists in the shot {name_shot}.")
            print("Keep first point with coordinates " +
                  f"{self.shots[name_shot].copoints[name_point]}")
            print(":--------------------------:")

        self.copoints[name_point].append(name_shot)

    def add_gcp(self, name_gcp: str, code_gcp: int, coor_gcp: np.array) -> None:
        """
        Add GCP in the Worksite

        Args:
        name_gcp (str): Name of the gcp.
        code_gcp (int): ign code to differentiate between support points (1, 2, 3)
                    and control points (11, 12, 13)
                    1 means precision in Z, 2 in X and Y and 3 in X, Y, Z.
        coor_gcp (numpy.array): Array of ground coordinate [X, Y, Z].
        """
        self.gcp[name_gcp] = GCP(name_gcp, code_gcp, coor_gcp)
