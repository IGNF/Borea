"""
Acquisition data class module.
"""
from typing import Union
import numpy as np
from scipy.spatial.transform import Rotation
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj
from src.altimetry.dem import Dem
from src.utils.conversion import change_dim


# pylint: disable-next=too-many-instance-attributes
class Shot:
    """
    Shot class definition.

    Args:
        name_shot (str): Name of the shot.
        pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
        ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa] in degree.
        name_cam (str): Name of the camera.
        unit_angle (str): unit of angle 'd' degrees, 'r' radian.
    """
    # pylint: disable-next=too-many-arguments
    def __init__(self, name_shot: str, pos_shot: np.ndarray,
                 ori_shot: np.ndarray, name_cam: str, unit_angle: str) -> None:
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.pos_shot_eucli = None
        self.ori_shot = ori_shot
        self.ori_shot_eucli = None
        self.unit_angle = unit_angle
        self.name_cam = name_cam
        self.copoints = {}
        self.gipoints = {}
        self.gcps = {}
        self.mat_rot = self.set_rot_shot()
        self.mat_rot_eucli = None
        self.projeucli = None
        self.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        self.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

    @classmethod
    # pylint: disable-next=too-many-arguments
    def from_param_euclidean(cls, name_shot: str, pos_eucli: np.ndarray,
                             mat_ori_eucli: np.ndarray, name_cam: str,
                             unit_angle: str, proj: ProjEngine) -> None:
        """
        Construction of a shot object using the Euclidean position.

        Args:
            name_shot (str): Name of the shot.
            pos_eucli (np.array): Euclidean position of the shot.
            mat_ori_eucli (np.array): Euclidean rotation matrix of the shot.
            name_cam (str): Name of the camera.
            proj (ProjEngine): Projection of the worksite.

        Returns:
            Shot: The shot.
        """
        shot = cls(name_shot, np.array([0, 0, 0]), np.array([0, 0, 0]), name_cam, unit_angle)
        shot.pos_shot_eucli = pos_eucli
        shot.projeucli = EuclideanProj(pos_eucli[0], pos_eucli[1], proj)
        unitori = shot.unit_angle == "d"
        shot.ori_shot_eucli = -Rotation.from_matrix(mat_ori_eucli).as_euler("xyz", degrees=unitori)
        shot.pos_shot = shot.projeucli.euclidean_to_world(shot.pos_shot_eucli[0],
                                                          shot.pos_shot_eucli[1],
                                                          shot.pos_shot_eucli[2])
        shot.copoints = {}
        shot.gcps = {}
        shot.gipoints = {}
        shot.mat_rot = shot.projeucli.mat_eucli_to_mat(shot.pos_shot[0], shot.pos_shot[1],
                                                       mat_ori_eucli)
        shot.mat_rot_eucli = mat_ori_eucli
        shot.ori_shot = -Rotation.from_matrix(shot.mat_rot).as_euler("xyz", degrees=unitori)

        shot.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        shot.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

        return shot

    def set_rot_shot(self) -> np.ndarray:
        """
        Build the rotation matrix with omega phi kappa.

        Returns:
            np.array: The rotation matrix.
        """
        if self.unit_angle == "d":
            ori_shot = np.copy(self.ori_shot)*np.pi/180
        else:
            ori_shot = self.ori_shot

        rx = np.array([[1, 0, 0],
                       [0, np.cos(ori_shot[0]), -np.sin(ori_shot[0])],
                       [0, np.sin(ori_shot[0]), np.cos(ori_shot[0])]])
        ry = np.array([[np.cos(ori_shot[1]), 0, np.sin(ori_shot[1])],
                       [0, 1, 0],
                       [-np.sin(ori_shot[1]), 0, np.cos(ori_shot[1])]])
        rz = np.array([[np.cos(ori_shot[2]), -np.sin(ori_shot[2]), 0],
                       [np.sin(ori_shot[2]), np.cos(ori_shot[2]), 0],
                       [0, 0, 1]])
        return (rx @ ry @ rz).T

    def set_param_eucli_shot(self, proj: ProjEngine) -> None:
        """
        Setting up Euclidean parameters projeucli, pos_shot_eucli, ori_shot_eucli, mat_rot_eucli.

        Args:
            proj (ProjEngine): Projection of the worksite.
        """
        self.projeucli = EuclideanProj(self.pos_shot[0], self.pos_shot[1], proj)
        self.pos_shot_eucli = self.projeucli.world_to_euclidean(self.pos_shot[0],
                                                                self.pos_shot[1],
                                                                self.pos_shot[2])
        self.mat_rot_eucli = self.projeucli.mat_to_mat_eucli(self.pos_shot[0],
                                                             self.pos_shot[1],
                                                             self.mat_rot)
        unitori = self.unit_angle == "d"
        self.ori_shot_eucli = -Rotation.from_matrix(self.mat_rot_eucli).as_euler('xyz',
                                                                                 degrees=unitori)

    # pylint: disable-next=too-many-arguments too-many-locals
    def world_to_image(self, x_world: Union[np.ndarray, float],
                       y_world: Union[np.ndarray, float],
                       z_world: Union[np.ndarray, float],
                       cam: Camera, dem: Dem,
                       type_z_data: str, type_z_shot: str) -> np.ndarray:
        """
        Calculates the c,l coordinates of a terrain point in an image.

        Args:
            x_world (Union[np.array, float]): the coordinate x of ground point.
            y_world (Union[np.array, float]): the coordinate y of ground point.
            z_world (Union[np.array, float]): the coordinate z of ground point.
            cam (Camera): the camera used.
            dem (Dem): Dem of the worksite.
            type_z_data (str): type of z of data.
                               "h" height
                               "a" altitude
            type_z_shot (str): type of z of worksite.
                               "h" height
                               "hl" height with linear alteration
                               "a" altitude / elevation
                               "al" altitude with linear alteration

        Returns:
            np.array: The image coordinate [c,l].
        """
        if len(type_z_data) != len(type_z_shot) and dem is None:
            raise ValueError("Missing dem, because type z data != type z shot.")

        if isinstance(x_world, np.ndarray):
            dim = np.shape(x_world)
        else:
            dim = ()

        p_eucli = self.projeucli.world_to_euclidean(x_world, y_world, z_world)
        pos_shot = np.array(self.conv_z_type_to_type(type_z_shot, type_z_data, cam, dem,
                                                     self.pos_shot[0],
                                                     self.pos_shot[1],
                                                     self.pos_shot[2]))
        pos_eucli = self.projeucli.world_to_euclidean(pos_shot[0], pos_shot[1], pos_shot[2])
        p_bundle = self.mat_rot_eucli @ np.vstack([p_eucli[0] - pos_eucli[0],
                                                   p_eucli[1] - pos_eucli[1],
                                                   p_eucli[2] - pos_eucli[2]])
        x_shot = p_bundle[0] * cam.focal / p_bundle[2]
        y_shot = p_bundle[1] * cam.focal / p_bundle[2]
        z_shot = p_bundle[2]
        x_shot, y_shot, z_shot = self.f_sys(x_shot, y_shot, z_shot)
        x_col = cam.ppax + x_shot
        y_lig = cam.ppay + y_shot
        return np.array([change_dim(x_col, dim), change_dim(y_lig, dim)])

    # pylint: disable-next=too-many-locals too-many-arguments
    def image_to_world(self, col: Union[np.ndarray, float], line: Union[np.ndarray, float],
                       cam: Camera, dem: Dem, type_z_data: str, type_z_shot: str) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            dem (Dem): Dem of the worksite.
            type_z_data (str): type of z data you want in output.
                               "h" height
                               "a" altitude / elevation
            type_z_shot (str): type of z shot, default = "a".
                          "h" height
                          "hl" height with linear alteration
                          "a" altitude / elevation
                          "al" altitude with linear alteration

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        if dem is None:
            raise ValueError("Missing dem")

        if isinstance(col, np.ndarray):
            dim = np.shape(col)
        else:
            dim = ()

        z_world = np.full_like(col, dem.get(self.pos_shot[0], self.pos_shot[1]))
        x_world, y_world, _ = self.image_z_to_world(col, line, cam, dem, type_z_shot, z_world)
        precision_reached = False
        nbr_iter = 0
        iter_max = 10
        while not precision_reached and nbr_iter < iter_max:
            z_world = dem.get(x_world, y_world)
            x_new_world, y_new_world, z_new_world = self.image_z_to_world(col, line, cam, dem,
                                                                          type_z_shot, z_world)
            x_diff = (x_new_world - x_world) ** 2
            y_diff = (y_new_world - y_world) ** 2
            z_diff = (z_new_world - z_world) ** 2
            dist2 = x_diff + y_diff + z_diff
            precision_reached = np.any(dist2 < 0.01**2)
            x_world, y_world, z_world = x_new_world, y_new_world, z_new_world
            nbr_iter += 1

        x_world, y_world, z_world = self.conv_z_type_to_type(dem.type_dem, type_z_data, cam,
                                                             dem, x_world, y_world, z_world)
        x_world = change_dim(x_world, dim)
        y_world = change_dim(y_world, dim)
        z_world = change_dim(z_world, dim)
        return np.array([x_world, y_world, z_world])

    # pylint: disable-next=too-many-locals too-many-arguments
    def image_z_to_world(self, col: Union[np.ndarray, float], line: Union[np.ndarray, float],
                         cam: Camera, dem: Dem, type_z_shot: str,
                         z: Union[np.ndarray, float] = 0) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            dem (Dem): Dem of the worksite.
            type_z_shot (str): type of z, default = "a".
                          "h" height
                          "hl" height with linear alteration
                          "a" altitude / elevation
                          "al" altitude with linear alteration
            z (Union[np.array, float]): La position z du point par défault = 0.

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        if isinstance(col, np.ndarray):
            dim = np.shape(col)
            if np.all(z == 0):
                z = np.full_like(col, 0)
        else:
            dim = ()

        x_bundle, y_bundle, z_bundle = self.image_to_bundle(col, line, cam)
        pos_shot = self.conv_z_type_to_type(type_z_shot, dem.type_dem, cam, dem,
                                            self.pos_shot[0], self.pos_shot[1], self.pos_shot[2])
        pos_eucli = self.projeucli.world_to_euclidean(pos_shot[0], pos_shot[1], pos_shot[2])
        p_local = self.mat_rot_eucli.T @ np.vstack([x_bundle, y_bundle, z_bundle])
        p_local = p_local + pos_eucli.reshape((3, 1))
        lamb = (z - pos_eucli[2])/(p_local[2] - pos_eucli[2])
        x_local = pos_eucli[0] + (p_local[0] - pos_eucli[0]) * lamb
        y_local = pos_eucli[1] + (p_local[1] - pos_eucli[1]) * lamb
        x_world, y_world, _ = self.projeucli.euclidean_to_world(x_local, y_local, z)
        return np.array([change_dim(x_world, dim), change_dim(y_world, dim), z])

    def image_to_bundle(self, col: Union[np.ndarray, float],
                        line: Union[np.ndarray, float], cam: Camera) -> np.ndarray:
        """
        Convert coordinate image col line to coordinate bundle.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        x_shot = col - cam.ppax
        y_shot = line - cam.ppay
        z_shot = np.full_like(x_shot, cam.focal)
        x_shot, y_shot, z_shot = self.f_sys_inv(x_shot, y_shot, z_shot)
        x_bundle = x_shot / cam.focal * z_shot
        y_bundle = y_shot / cam.focal * z_shot
        z_bundle = z_shot
        return np.array([x_bundle, y_bundle, z_bundle])

    def tranform_height(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float],
                        z: Union[np.ndarray, float]) -> float:
        """
        Converting z in altitude to z in height of point.

        Args:
            x (Union[np.array, float]): x coordinate of the point.
            y (Union[np.array, float]): x coordinate of the point.
            z (Union[np.array, float]): x coordinate of the point.

        Returns:
            float: New height z.
        """
        coor_geog = self.projeucli.proj_engine.tf.carto_to_geog(x, y, z)
        try:
            new_z = self.projeucli.proj_engine.tf.geog_to_geoid(coor_geog[0],
                                                                coor_geog[1],
                                                                coor_geog[2])[2]
        except AttributeError:
            print("Warning: the geoid has not been entered, the z transformation from altitude "
                  "to height has not been performed, return z altitude")
            new_z = z

        if new_z == np.inf:
            raise ValueError("out geoid")
        return new_z

    def tranform_altitude(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float],
                          z: Union[np.ndarray, float]) -> float:
        """
        Converting z in height to z in altitude of point.

        Args:
            x (Union[np.array, float]): x coordinate of the point.
            y (Union[np.array, float]): x coordinate of the point.
            z (Union[np.array, float]): x coordinate of the point.

        Returns:
            float: New altitude z.
        """
        coor_geog = self.projeucli.proj_engine.tf.carto_to_geog(x, y, z)
        try:
            coor_geog = self.projeucli.proj_engine.tf.geoid_to_geog(coor_geog[0],
                                                                    coor_geog[1],
                                                                    coor_geog[2])
            new_z = self.projeucli.proj_engine.tf.geog_to_carto(coor_geog[0],
                                                                coor_geog[1],
                                                                coor_geog[2])[2]
        except AttributeError:
            print("Warning: the geoid has not been entered, the z transformation from height "
                  "to altitude has not been performed, return z height")
            new_z = z

        if np.all(new_z == np.inf):
            raise ValueError("out geoid")
        return new_z

    def get_z_remove_scale_factor(self, z_nadir: float) -> float:
        """
        Return Z after removing the scale factor. The Z of the object is NOT modified.

        Args:
            z_nadir (float): Z nadir of the shot

        Returns:
            float: z without linear alteration
        """
        scale_factor = self.projeucli.proj_engine.get_scale_factor(self.pos_shot[0],
                                                                   self.pos_shot[1])
        return (self.pos_shot[2] + scale_factor * z_nadir) / (1 + scale_factor)

    def get_z_add_scale_factor(self, z_nadir: float) -> float:
        """
        Return Z after adding the scale factor. The Z of the object is NOT modified.

        Args:
            z_nadir (float): Z nadir of the shot

        Returns:
            float: z with linear alteration.
        """
        scale_factor = self.projeucli.proj_engine.get_scale_factor(self.pos_shot[0],
                                                                   self.pos_shot[1])
        return self.pos_shot[2] + scale_factor * (self.pos_shot[2] - z_nadir)

    # pylint: disable-next=too-many-arguments
    def conv_z_type_to_type(self, type_actual: str, type_expected: str, cam: Camera, dem: Dem,
                            x: Union[np.ndarray, float], y: Union[np.ndarray, float],
                            z: Union[np.ndarray, float]) -> float:
        """
        Convert z from one type to another.

        Args:
            type_actual (str): type z input.
                               "h" height
                               "hl" height with linear alteration
                               "a" altitude / elevation
                               "al" altitude with linear alteration
            type_expected (str): type z output.
                                 "h" height
                                 "hl" height with linear alteration
                                 "a" altitude / elevation
                                 "al" altitude with linear alteration
            cam (Camera): The camera of the shot.
            dem (Dem): Dem of the worksite.
            x (Union[np.array, float]): x coordinate of the point.
            y (Union[np.array, float]): x coordinate of the point.
            z (Union[np.array, float]): x coordinate of the point.

        Returns:
            tuple: X, Y, Z with z in type expected
        """
        conv = {"a-h": [[self.tranform_height, 0]],
                "h-a": [[self.tranform_altitude, 0]],
                "al-h": [[self.get_z_remove_scale_factor, 1], [self.tranform_height, 0]],
                "h-al": [[self.tranform_altitude, 0], [self.get_z_add_scale_factor, 2]],
                "a-hl": [[self.tranform_height, 0], [self.get_z_add_scale_factor, 2]],
                "hl-a": [[self.get_z_remove_scale_factor, 1], [self.tranform_altitude, 0]],
                "al-hl": [[self.tranform_height, 0]],
                "hl-al": [[self.tranform_altitude, 0]],
                "al-a": [[self.get_z_remove_scale_factor, 1]],
                "a-al": [[self.get_z_add_scale_factor, 2]],
                "hl-h": [[self.get_z_remove_scale_factor, 1]],
                "h-hl": [[self.get_z_add_scale_factor, 2]]}
        id_type = f"{type_actual}-{type_expected}"
        if type_actual != type_expected:
            list_func = conv[id_type]
            if len(id_type) == 4:
                for func in list_func:
                    if func[1] == 2:
                        z_nadir = self.image_to_world(cam.ppax, cam.ppay, cam,
                                                      dem, type_expected[0], type_expected[0])[2]
                        z = func[0](z_nadir)
                    elif func[1] == 1:
                        z_nadir = self.image_to_world(cam.ppax, cam.ppay, cam,
                                                      dem, type_actual[0], type_actual[0])[2]
                        z = func[0](z_nadir)
                    else:
                        z = func[0](x, y, z)
            else:
                z = list_func[0][0](x, y, z)

        return x, y, z
