"""
Worksite data class module
"""
import sys
import json
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.gcp import GCP
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


# pylint: disable-next=too-many-instance-attributes
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
        self.check_cop = False
        self.gcps = {}
        self.check_gcp = False
        self.proj = None
        self.projeucli = None

    def add_shot(self, name_shot: str, pos_shot: np,
                 ori_shot: np, name_cam: str) -> None:
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

    def set_proj(self, epsg: str, file_epsg: str = None) -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (str): Code epsg of the porjection ex: "EPSG:2154".
            file_epsg (str): Path to the json which list projection
        """
        if file_epsg is None:
            self.set_projection(epsg)
        else:
            try:
                with open(file_epsg, 'r', encoding="utf-8") as json_file:
                    projection_list = json.load(json_file)
                    json_file.close()
                try:
                    dict_epsg = projection_list[epsg]
                    self.proj = ProjEngine(epsg, dict_epsg)
                    coor_barycentre = self.calculate_barycentre()
                    self.projeucli = EuclideanProj(coor_barycentre[0],
                                                   coor_barycentre[1],
                                                   self.proj)
                except KeyError:
                    self.set_projection(epsg)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"The path {file_epsg} is incorrect !!!") from e

    def set_projection(self, epsg: str = "EPSG:2154") -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (str): Code epsg of the porjection ex: "EPSG:2154".
        """
        path_data = "./src/data/projection_list.json"
        with open(path_data, 'r', encoding="utf-8") as json_file:
            projection_list = json.load(json_file)
            json_file.close()
        try:
            dict_epsg = projection_list[epsg]
            self.proj = ProjEngine(epsg, dict_epsg)
            coor_barycentre = self.calculate_barycentre()
            self.projeucli = EuclideanProj(coor_barycentre[0], coor_barycentre[1], self.proj)
        except KeyError:
            self.proj = ProjEngine(epsg)

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

    def add_gcp(self, name_gcp: str, code_gcp: int, coor_gcp: np) -> None:
        """
        Add GCP in the Worksite

        Args:
        name_gcp (str): Name of the gcp.
        code_gcp (int): ign code to differentiate between support points (1, 2, 3)
                    and control points (11, 12, 13)
                    1 means precision in Z, 2 in X and Y and 3 in X, Y, Z.
        coor_gcp (numpy.array): Array of ground coordinate [X, Y, Z].
        """
        self.gcps[name_gcp] = GCP(name_gcp, code_gcp, coor_gcp)

    def calculate_coor_img_gcp(self) -> None:
        """
        Calculates the position of gcps in the images they appear in
        """
        if self.check_gcp:
            if self.check_cop:
                for name_gcp in list(self.gcps):
                    try:
                        list_shots = self.copoints[name_gcp]
                        gcp = self.gcps[name_gcp]
                        for name_shot in list_shots:
                            shot = self.shots[name_shot]
                            cam = self.cameras[shot.name_cam]
                            coor_img = shot.world_to_image(gcp.coor, cam, self.projeucli)
                            self.shots[name_shot].gcps[name_gcp] = coor_img
                    except KeyError:
                        self.shots[name_shot].gcps = {}
                        print("The calculation of the gcps image coordinates could not be done.")
                        print("Point(s) is/are not known on an image.")

    def calculate_barycentre(self) -> np.array:
        """
        Calculate barycentre of the worksite
        """
        size = len(self.shots)
        pos = np.zeros((size, 3))
        i = 0
        for shot in self.shots.values():
            pos[i, :] = shot.pos_shot
            i += 1
        return np.mean(pos, axis=0)
