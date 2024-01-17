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
        self.cop_ground = {}
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

    def set_proj(self, epsg: str, file_epsg: str = None, path_geotiff: str = None) -> None:
        """
        Setup a projection system to the worksite.

        Args:
            epsg (str): Code epsg of the porjection ex: "EPSG:2154".
            file_epsg (str): Path to the json which list projection.
            path_geotiff (str): List of GeoTIFF which represents the ellipsoid in grid form.
        """
        if file_epsg is None:
            self.set_projection(epsg, path_geotiff)
        else:
            try:
                with open(file_epsg, 'r', encoding="utf-8") as json_file:
                    projection_list = json.load(json_file)
                    json_file.close()
                try:
                    dict_epsg = projection_list[epsg]
                    self.proj = ProjEngine(epsg, dict_epsg, path_geotiff)
                    coor_barycentre = self.calculate_barycentre()
                    self.projeucli = EuclideanProj(coor_barycentre[0],
                                                   coor_barycentre[1],
                                                   self.proj)
                except KeyError:
                    self.set_projection(epsg, path_geotiff)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"The path {file_epsg} is incorrect !!!") from e

    def set_projection(self, epsg: str = "EPSG:2154", path_geotiff: str = None) -> None:
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
        Add GCP in the Worksite.

        Args:
            name_gcp (str): Name of the gcp.
            code_gcp (int): IGN code to differentiate between support points (1, 2, 3)
                            and control points (11, 12, 13)
                            1 means precision in Z, 2 in X and Y and 3 in X, Y, Z.
            coor_gcp (numpy.array): Array of ground coordinate [X, Y, Z].
        """
        self.gcps[name_gcp] = GCP(name_gcp, code_gcp, coor_gcp)

    def calculate_world_to_image_gcp(self, lcode: list) -> None:
        """
        Calculates the position of gcps which corresponds to the data code
        in the images they appear in.

        Args:
            lcode (list): gcp code.
        """
        if self.check_gcp and self.check_cop:
            for name_gcp in list(self.gcps):
                if self.gcps[name_gcp].code in lcode:
                    try:
                        list_shots = self.copoints[name_gcp]
                        gcp = self.gcps[name_gcp]
                        for name_shot in list_shots:
                            shot = self.shots[name_shot]
                            cam = self.cameras[shot.name_cam]
                            coor_img = shot.world_to_image(gcp.coor, cam, self.projeucli)
                            self.shots[name_shot].gcps[name_gcp] = coor_img
                    except KeyError:
                        continue

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

    def calculate_image_world_copoints(self) -> None:
        """
        Calculates the ground position of connecting point by intersection with
        the most distance between two shots
        """
        if self.check_cop:
            for name_cop in list(self.copoints):  # Loop on copoints
                shot1 = ""
                shot2 = ""
                dist = 0
                list_shot1 = self.copoints[name_cop]
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
                coor = self.eucli_intersection_2p(name_cop, self.shots[shot1], self.shots[shot2])
                coor = self.projeucli.euclidean_to_world(coor[0], coor[1], coor[2])
                self.cop_ground[name_cop] = coor

    # pylint: disable-next=too-many-locals
    def eucli_intersection_2p(self, name_copoint: str, shot1: Shot, shot2: Shot) -> np.array:
        """
        Calculates the euclidien position of a point from two shots

        Args:
            name_copoint (str): name of copoint to calcule coordinate
            shot1 (Shot): Frist shot
            shot2 (Shot): Second shot

        Returns:
            np.array: Euclidien coordinate of the copoint
        """
        p_img1 = shot1.copoints[name_copoint]
        p_img2 = shot2.copoints[name_copoint]
        cam1 = self.cameras[shot1.name_cam]
        cam2 = self.cameras[shot2.name_cam]
        pos_eucli1 = self.projeucli.world_to_euclidean(shot1.pos_shot[0],
                                                       shot1.pos_shot[1],
                                                       shot1.pos_shot[2])
        pos_eucli2 = self.projeucli.world_to_euclidean(shot2.pos_shot[0],
                                                       shot2.pos_shot[1],
                                                       shot2.pos_shot[2])
        mat_eucli1 = self.projeucli.mat_to_mat_eucli(shot1.pos_shot[0],
                                                     shot1.pos_shot[1],
                                                     shot1.mat_rot).T
        mat_eucli2 = self.projeucli.mat_to_mat_eucli(shot2.pos_shot[0],
                                                     shot2.pos_shot[1],
                                                     shot2.mat_rot).T
        base = pos_eucli1 - pos_eucli2
        vect1 = mat_eucli1 @ np.array([p_img1[0] - cam1.ppax,
                                       p_img1[1] - cam1.ppay,
                                       -cam1.focal])
        vect2 = mat_eucli2 @ np.array([p_img2[0] - cam2.ppax,
                                       p_img2[1] - cam2.ppay,
                                       -cam2.focal])
        norme_v1 = vect1 @ vect1
        norme_v2 = vect2 @ vect2
        v1_v2 = vect1 @ vect2
        b_v1 = base @ vect1
        b_v2 = base @ vect2
        p1_eucli = pos_eucli1 + ((b_v2*v1_v2 - b_v1*norme_v1)/(v1_v2**2 - norme_v1*norme_v2))*vect1
        p2_eucli = pos_eucli2 + ((b_v2*norme_v1 - b_v1*v1_v2)/(v1_v2**2 - norme_v1*norme_v2))*vect2
        return 0.5 * (p1_eucli + p2_eucli)

    # pylint: disable-next=pointless-string-statement
    """
    def calculate_coor_ground_copoints2(self) -> None:
        ""
        Calculates the ground position of connecting point by least-squares method
        ""
        if self.check_cop:
            # Initinialisation of parameter
            init_param = {}
            for shot in self.shots.values(): # Loop on shots
                cop_param = {}
                for cop in list(shot.copoints): # Loop on copoints of the shot
                    x,y,z = shot.image_to_world(shot.copoints[0],
                                                shot.copoints[1],
                                                self.cameras[shot.name_cam],
                                                self.projeucli)
                    cop_param[cop] = self.projeucli.world_to_euclidean(x,y,z)
                init_param[shot] = cop_param
    """
