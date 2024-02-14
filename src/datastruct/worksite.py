"""
Worksite data class module.
"""
import sys
import json
import numpy as np
from pyproj import CRS, exceptions
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.gcp import GCP
from src.geodesy.proj_engine import ProjEngine
from src.position.shot_pos import space_resection
from src.altimetry.dem import Dem


# pylint: disable-next=too-many-instance-attributes
class Worksite:
    """
    Worksite class.
    """
    def __init__(self, name: str) -> None:
        """
        Class definition of Worksite.

        Args:
            name (str): Name of the worksite.
        """
        self.name = name
        self.shots = {}
        self.cameras = {}
        self.copoints = {}
        self.check_cop = False
        self.gipoints = {}
        self.check_gip = False
        self.gcps = {}
        self.check_gcp = False
        self.cop_world = {}
        self.gip_world = {}
        self.proj = None
        self.dem = None
        self.type_z_data = None
        self.type_z_shot = None

    # pylint: disable-next=too-many-arguments
    def add_shot(self, name_shot: str, pos_shot: np.ndarray,
                 ori_shot: np.ndarray, name_cam: str, unit_angle: str) -> None:
        """
        Add Shot to the attribut Shots.

        Args:
            name_shot (str): Name of the shot.
            pos_shot (np.array): Array of coordinate position [X, Y, Z].
            ori_shot (np.array): Array of orientation of the shot [Omega, Phi, Kappa].
            name_cam (str): Name of the camera.
            unit_angle (str): unit of angle 'd' degrees, 'r' radian.
        """
        self.shots[name_shot] = Shot(name_shot=name_shot,
                                     pos_shot=pos_shot,
                                     ori_shot=ori_shot,
                                     name_cam=name_cam,
                                     unit_angle=unit_angle)

    def set_proj(self, epsg: str, file_epsg: str = None, path_geotiff: str = None) -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (str): Code epsg of the porjection ex: "EPSG:2154".
            file_epsg (str): Path to the json which list projection.
            path_geotiff (str): List of GeoTIFF which represents the ellipsoid in grid form.
        """
        try:  # Check if the epsg exist
            if epsg[0:5] != "EPSG:":
                epsg = "EPSG:" + epsg
            crs = CRS.from_string(epsg)
            del crs
        except exceptions.CRSError as e_info:
            raise exceptions.CRSError(f"Your {epsg} doesn't exist") from e_info

        if file_epsg is None:
            self.known_projection(epsg, path_geotiff)
        else:
            try:
                with open(file_epsg, 'r', encoding="utf-8") as json_file:
                    projection_list = json.load(json_file)
                    json_file.close()
                try:
                    dict_epsg = projection_list[epsg]
                    self.proj = ProjEngine(epsg, dict_epsg, path_geotiff)
                    self.set_param_eucli_shots()
                except KeyError:
                    self.known_projection(epsg, path_geotiff)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"The path {file_epsg} is incorrect !!!") from e

    def known_projection(self, epsg: str = "EPSG:2154", path_geotiff: str = None) -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (str): Code epsg of the porjection ex: "EPSG:2154".
            path_geotiff (str): List of GeoTIFF which represents the ellipsoid in grid form.
        """
        path_data = "./src/data/projection_list.json"
        with open(path_data, 'r', encoding="utf-8") as json_file:
            projection_list = json.load(json_file)
            json_file.close()
        try:
            dict_epsg = projection_list[epsg]
            self.proj = ProjEngine(epsg, dict_epsg, path_geotiff)
            self.set_param_eucli_shots()
        except KeyError:
            self.proj = ProjEngine(epsg)

    def set_param_eucli_shots(self) -> None:
        """
        Setting up Euclidean parameters pos_shot_eucli, ori_shot_eucli, mat_rot_eucli by shot.
        """
        for shot in self.shots.values():
            shot.set_param_eucli_shot(self.proj)

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

    def add_copoint(self, name_point: str, name_shot: str, x: float, y: float) -> None:
        """
        Add linking point between acquisition in two part.
        One in self.copoints a dict with name_point the key and list of acquisition the result.
        And One in self.shot[name_shot].copoints a dict whit
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

        if name_point not in self.copoints:
            self.copoints[name_point] = []

        if name_point not in self.shots[name_shot].copoints:
            self.shots[name_shot].copoints[name_point] = [x, y]
        else:
            print("\n :--------------------------:")
            print("Warning : connecting point duplicate.")
            print(f"The point {name_point} already exists in the shot {name_shot}.")
            print("Keep first point with coordinates " +
                  f"{self.shots[name_shot].copoints[name_point]}.")
            print(":--------------------------:")

        self.copoints[name_point].append(name_shot)

    def add_gipoint(self, name_point: str, name_shot: str, x: float, y: float) -> None:
        """
        Add linking point between acquisition in two part.
        One in self.gipoints a dict with name_point the key and list of acquisition the result.
        And One in self.shot[name_shot].gipoints a dict whit
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

        if name_point not in self.gipoints:
            self.gipoints[name_point] = []

        if name_point not in self.shots[name_shot].gipoints:
            self.shots[name_shot].gipoints[name_point] = [x, y]
        else:
            print("\n :--------------------------:")
            print("Warning : connecting point duplicate.")
            print(f"The point {name_point} already exists in the shot {name_shot}.")
            print("Keep first point with coordinates " +
                  f"{self.shots[name_shot].gipoints[name_point]}.")
            print(":--------------------------:")

        self.gipoints[name_point].append(name_shot)

    def add_gcp(self, name_gcp: str, code_gcp: int, coor_gcp: np.ndarray) -> None:
        """
        Add GCP in the Worksite.

        Args:
            name_gcp (str): Name of the gcp.
            code_gcp (int): IGN code to differentiate between support points (1, 2, 3)
                            and control points (11, 12, 13)
                            1 means precision in Z, 2 in X and Y and 3 in X, Y, Z.
            coor_gcp (numpy.array): Array of ground coordinate [X, Y, Z].
        """
        self.gcps[name_gcp] = GCP(name_gcp, code_gcp, coor_gcp)

    def add_dem(self, path_dem: str, type_dem: str) -> None:
        """
        Add class DEM to the worksite.

        Args:
            path_dem (str): Path to the dem.
            type (str): Type of the dem "altitude" or "height".
        """
        if type_dem not in ["altitude", "height"]:
            raise ValueError(f"The dem's type {type_dem} isn't correct ('altitude' or 'height')")

        if type_dem == "altitude":
            type_dem = "a"
        else:
            type_dem = "h"

        self.dem = Dem(path_dem, type_dem)

    def calculate_world_to_image_gcp(self, lcode: list) -> None:
        """
        Calculates the position of gcps which corresponds to the data code
        in the images they appear in.

        Args:
            lcode (list): gcp code.
        """
        if self.check_gcp and self.check_gip:
            for name_gcp, gcp in self.gcps.items():
                if gcp.code in lcode or lcode == []:
                    try:
                        list_shots = self.gipoints[name_gcp]
                        for name_shot in list_shots:
                            shot = self.shots[name_shot]
                            cam = self.cameras[shot.name_cam]
                            coor_img = shot.world_to_image(gcp.coor[0], gcp.coor[1], gcp.coor[2],
                                                           cam, self.dem, self.type_z_data,
                                                           self.type_z_shot)
                            self.shots[name_shot].gcps[name_gcp] = coor_img
                    except KeyError:
                        continue

    def calculate_barycentre(self) -> np.ndarray:
        """
        Calculate barycentre of the worksite.

        Returns:
            np.array: The barycentre [X, Y, Z].
        """
        size = len(self.shots)
        pos = np.zeros((size, 3))
        i = 0
        for shot in self.shots.values():
            pos[i, :] = shot.pos_shot
            i += 1
        return np.mean(pos, axis=0)

    # pylint: disable-next=too-many-locals too-many-branches
    def calculate_init_image_world(self, type_point: str = "copoint",
                                   control_type: list = None) -> None:
        """
        Calculates the ground position of connecting point by intersection with
        the most distance between two shots or ground image point.

        Args:
            type_point (str): "copoint" or "gipoint" depending on what you want to calculate.
            control_type (list): type controle for gcp.
        """
        if control_type is None:
            control_type = []

        check = False
        if type_point == "copoint":
            points = self.copoints
            check = self.check_cop
            check_gcp = False

        else:
            if type_point == "gipoint":
                points = self.gipoints
                check = self.check_gip
                check_gcp = True

        if check:
            for name_p, item_p in points.items():  # Loop on points
                if check_gcp:
                    if control_type != []:
                        if self.gcps[name_p].code not in control_type:
                            continue
                if len(item_p) == 1:
                    continue
                shot1 = ""
                shot2 = ""
                dist = 0
                list_shot1 = item_p.copy()
                list_shot2 = list_shot1.copy()
                _ = list_shot1.pop(-1)
                for name_shot1 in list_shot1:  # Double loop on shots of copoint
                    _ = list_shot2.pop(0)
                    for name_shot2 in list_shot2:
                        pos_shot1 = self.shots[name_shot1].pos_shot
                        pos_shot2 = self.shots[name_shot2].pos_shot
                        new_dist = np.sqrt(np.sum((pos_shot1 - pos_shot2)**2))
                        if new_dist > dist:
                            dist = new_dist
                            shot1 = name_shot1
                            shot2 = name_shot2
                coor = self.eucli_intersection_2p(name_p, self.shots[shot1], self.shots[shot2])
                if type_point == "copoint":
                    self.cop_world[name_p] = coor
                if type_point == "gipoint":
                    self.gip_world[name_p] = coor
        else:
            print(f"There isn't {type_point} or bad spelling copoint / gipoint.")

    # pylint: disable-next=too-many-locals
    def eucli_intersection_2p(self, name_point: str, shot1: Shot, shot2: Shot) -> np.ndarray:
        """
        Calculates the euclidien position of a point from two shots.

        Args:
            name_point (str): Name of copoint to calcule coordinate.
            shot1 (Shot): Frist shot.
            shot2 (Shot): Second shot.

        Returns:
            np.array: Euclidien coordinate of the copoint.
        """
        if name_point in list(shot1.copoints):
            p_img1 = shot1.copoints[name_point]
            p_img2 = shot2.copoints[name_point]
        else:
            p_img1 = shot1.gipoints[name_point]
            p_img2 = shot2.gipoints[name_point]

        cam1 = self.cameras[shot1.name_cam]
        cam2 = self.cameras[shot2.name_cam]
        base = shot1.pos_shot - shot2.pos_shot
        vect1 = shot1.mat_rot.T @ shot1.image_to_bundle(p_img1[0], p_img1[1], cam1)
        vect2 = shot2.mat_rot.T @ shot2.image_to_bundle(p_img2[0], p_img2[1], cam2)
        norme_v1 = vect1 @ vect1
        norme_v2 = vect2 @ vect2
        v1_v2 = vect1 @ vect2
        b_v1 = base @ vect1
        b_v2 = base @ vect2
        num1 = b_v2*v1_v2 - b_v1*norme_v2
        num2 = b_v2*norme_v1 - b_v1*v1_v2
        denum = v1_v2**2 - norme_v1*norme_v2
        p1_world = shot1.pos_shot + ((num1)/(denum))*vect1
        p2_world = shot2.pos_shot + ((num2)/(denum))*vect2
        return (p1_world + p2_world) / 2

    def shootings_position(self, add_pixel: tuple = (0, 0)) -> None:
        """
        Recalculates the shot's 6 external orientation parameters,
        the 3 angles omega, phi, kappa and its position x, y, z.
        For all shot with a variation pixel.

        Args:
            add_pixel (tuple): Factor (column, line) added on observable point.
        """
        for key_shot, item_shot in self.shots.items():
            cam = self.cameras[item_shot.name_cam]
            self.shots[key_shot] = space_resection(item_shot, cam, self.proj,
                                                   self.dem, self.type_z_data,
                                                   self.type_z_shot, add_pixel)
