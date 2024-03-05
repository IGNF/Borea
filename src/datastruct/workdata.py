"""
Workdata data class module.
"""
import os
import sys
import json
from pathlib import Path, PureWindowsPath
import numpy as np
from pyproj import CRS, exceptions
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.gcp import GCP
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm


# pylint: disable-next=too-many-instance-attributes
class Workdata:
    """
    Workdata class.
    """
    def __init__(self, name: str) -> None:
        """
        Class definition of Workdata.

        Args:
            name (str): Name of the worksite.
        """
        self.name = name
        self.shots = {}
        self.cameras = {}
        self.co_points = {}
        self.ground_img_pts = {}
        self.gcps = {}
        self.co_pts_world = {}
        self.img_pts_world = {}
        self.type_z_data = None
        self.type_z_shot = None
        self.approxeucli = False

    # pylint: disable-next=too-many-arguments
    def add_shot(self, name_shot: str, pos_shot: np.ndarray,
                 ori_shot: np.ndarray, name_cam: str,
                 unit_angle: str, linear_alteration: bool) -> None:
        """
        Add Shot to the attribut Shots.

        Args:
            name_shot (str): Name of the shot.
            pos_shot (np.array): Array of coordinate position [X, Y, Z].
            ori_shot (np.array): Array of orientation of the shot [Omega, Phi, Kappa].
            name_cam (str): Name of the camera.
            unit_angle (str): Unit of angle 'degrees', 'radian'.
            linear_alteration (bool): True if z shot is correct of linear alteration.
        """
        self.shots[name_shot] = Shot(name_shot=name_shot,
                                     pos_shot=pos_shot,
                                     ori_shot=ori_shot,
                                     name_cam=name_cam,
                                     unit_angle=unit_angle,
                                     linear_alteration=linear_alteration)

    def set_proj(self, epsg: int, file_epsg: str = None, path_geotiff: str = None) -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (int): Code epsg of the porjection ex: 2154.
            file_epsg (str): Path to the json which list projection.
            path_geotiff (str): List of GeoTIFF which represents the ellipsoid in grid form.
        """
        ProjEngine.clear()
        try:  # Check if the epsg exist
            crs = CRS.from_epsg(epsg)
            del crs
        except exceptions.CRSError as e_info:
            raise exceptions.CRSError(f"Your EPSG:{epsg} doesn't exist") from e_info

        path_geotiff = Path(PureWindowsPath(path_geotiff)) if path_geotiff else None
        if not file_epsg:
            self.known_projection(epsg, path_geotiff)
        else:
            try:
                with open(Path(PureWindowsPath(file_epsg)), 'r', encoding="utf-8") as json_file:
                    projection_list = json.load(json_file)
                    json_file.close()
                try:
                    dict_epsg = projection_list[f"EPSG:{epsg}"]
                    ProjEngine().set_epsg(epsg, dict_epsg, path_geotiff)
                except KeyError:
                    self.known_projection(epsg, path_geotiff)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"The path {file_epsg} is incorrect !!!") from e

    def known_projection(self, epsg: int = 2154, path_geotiff: Path = None) -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (int): Code epsg of the porjection ex: "EPSG:2154".
            path_geotiff (Path): List of GeoTIFF which represents the ellipsoid in grid form.
        """
        path_data = os.path.join(os.path.dirname(__file__), "..", "..",
                                 "resources", "projection_list.json")
        with open(path_data, 'r', encoding="utf-8") as json_file:
            projection_list = json.load(json_file)
            json_file.close()
        try:
            dict_epsg = projection_list[f"EPSG:{epsg}"]
            ProjEngine().set_epsg(epsg, dict_epsg, path_geotiff)
        except KeyError:
            ProjEngine().set_epsg(epsg)

    # pylint: disable-next=too-many-arguments
    def add_camera(self, name_camera: str, ppax: float, ppay: float,
                   focal: float, width: float, height: float) -> None:
        """
        Add data camera in the Worksite.

        Args:
            name_camera (str): Name of the camera.
            ppax (float): Center of distortion in x.
            ppay (float): Center of distortion in y.
            focal (float): Focal of the camera.
            width (float): Width of the image camera.
            height (float): Height of the image camera.
        """
        self.cameras[name_camera] = Camera(name_camera=name_camera,
                                           ppax=ppax,
                                           ppay=ppay,
                                           focal=focal,
                                           width=width,
                                           height=height)

    def add_co_point(self, name_point: str, name_shot: str, x: float, y: float) -> None:
        """
        Add linking point between acquisition in two part.
        One in self.co_points a dict with name_point the key and list of acquisition the result.
        And One in self.shot[name_shot].co_points a dict whit
        name_point the key and list of coordinate x (column) y (line) the result in list.

        Agrs:
            name_point (str): Name of the connecting point.
            name_shot (str): Name of the acquisition.
            x (float): Pixel position of the point in column.
            y (float): Pixel position of the point in line.
        """
        if name_shot not in self.shots:
            print(f"The shot {name_shot} doesn't exist in list of shots.")
            sys.exit()

        if name_point not in self.co_points:
            self.co_points[name_point] = []

        if name_point not in self.shots[name_shot].co_points:
            self.shots[name_shot].co_points[name_point] = [x, y]
        else:
            print("\n :--------------------------:")
            print("Warning : connecting point duplicate.")
            print(f"The point {name_point} already exists in the shot {name_shot}.")
            print("Keep first point with coordinates " +
                  f"{self.shots[name_shot].co_points[name_point]}.")
            print(":--------------------------:")

        self.co_points[name_point].append(name_shot)

    def add_ground_img_pt(self, name_point: str, name_shot: str, x: float, y: float) -> None:
        """
        Add linking point between acquisition in two part.
        One in self.ground_img_pts a dict with name_point the key
        and list of acquisition the result.
        And One in self.shot[name_shot].ground_img_pts a dict whit
        name_point the key and list of coordinate x (column) y (line) the result in list.

        Agrs:
            name_point (str): Name of the connecting point.
            name_shot (str): Name of the acquisition.
            x (float): Pixel position of the point in column.
            y (float): Pixel position of the point in line.
        """
        try:
            self.shots[name_shot]
        except KeyError as e_info:
            raise ValueError(f"The shot {name_shot} doesn't exist in list of shots.") from e_info

        if name_point not in self.ground_img_pts:
            self.ground_img_pts[name_point] = []

        if name_point not in self.shots[name_shot].ground_img_pts:
            self.shots[name_shot].ground_img_pts[name_point] = [x, y]
        else:
            print("\n :--------------------------:")
            print("Warning : connecting point duplicate.")
            print(f"The point {name_point} already exists in the shot {name_shot}.")
            print("Keep first point with coordinates " +
                  f"{self.shots[name_shot].ground_img_pts[name_point]}.")
            print(":--------------------------:")

        self.ground_img_pts[name_point].append(name_shot)

    def add_gcp(self, name_gcp: str, code_gcp: int, coor_gcp: np.ndarray) -> None:
        """
        Add GCP in the Worksite.

        Args:
            name_gcp (str): Name of the gcp.
            code_gcp (int): IGN code to differentiate between support points (1, 2, 3)
                            and control points (11, 12, 13).
                            1 means precision in Z, 2 in X and Y and 3 in X, Y, Z.
            coor_gcp (numpy.array): Array of ground coordinate [X, Y, Z].
        """
        self.gcps[name_gcp] = GCP(name_gcp, code_gcp, coor_gcp)

    def set_dtm(self, path_dtm: str, type_dtm: str) -> None:
        """
        set class DtM to the worksite.

        Args:
            path_dtm (str): Path to the dtm.
            type (str): Type of the dtm "altitude" or "height".
        """
        if type_dtm not in ["altitude", "height", "a", "h"]:
            raise ValueError(f"The dtm's type {type_dtm} isn't correct ('altitude' or 'height')")

        Dtm.clear()
        Dtm().set_dtm(path_dtm, type_dtm)

    def set_approx_eucli_proj(self, approx: bool) -> None:
        """
        Setup approxeucli in worksite

        Args:
            apprx (bool): True if there are not projengine
        """
        self.approxeucli = approx
