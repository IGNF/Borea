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
    """
    def __init__(self, name_shot: str, pos_shot: np.array,
                 ori_shot: np.array, name_cam: str) -> None:
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.pos_shot_eucli = None
        self.ori_shot = ori_shot
        self.ori_shot_eucli = None
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
    def from_param_euclidean(cls, name_shot: str, pos_eucli: np.array,
                             mat_ori_eucli: np.array, name_cam: str,
                             proj: ProjEngine) -> None:
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
        shot = cls(name_shot, np.array([0, 0, 0]), np.array([0, 0, 0]), name_cam)
        shot.pos_shot_eucli = pos_eucli
        shot.projeucli = EuclideanProj(pos_eucli[0], pos_eucli[1], proj)
        shot.ori_shot_eucli = -Rotation.from_matrix(mat_ori_eucli).as_euler("xyz", degrees=True)
        shot.pos_shot = shot.projeucli.euclidean_to_world(shot.pos_shot_eucli[0],
                                                          shot.pos_shot_eucli[1],
                                                          shot.pos_shot_eucli[2])
        shot.copoints = {}
        shot.gcps = {}
        shot.gipoints = {}
        shot.mat_rot = shot.projeucli.mat_eucli_to_mat(shot.pos_shot[0], shot.pos_shot[1],
                                                       mat_ori_eucli)
        shot.mat_rot_eucli = mat_ori_eucli
        shot.ori_shot = -Rotation.from_matrix(shot.mat_rot).as_euler("xyz", degrees=True)

        shot.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        shot.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

        return shot

    def set_rot_shot(self) -> np.array:
        """
        Build the rotation matrix with omega phi kappa.

        Returns:
            np.array: The rotation matrix.
        """
        rx = np.array([[1, 0, 0],
                       [0, np.cos(self.ori_shot[0]*np.pi/180), -np.sin(self.ori_shot[0]*np.pi/180)],
                       [0, np.sin(self.ori_shot[0]*np.pi/180), np.cos(self.ori_shot[0]*np.pi/180)]])
        ry = np.array([[np.cos(self.ori_shot[1]*np.pi/180), 0, np.sin(self.ori_shot[1]*np.pi/180)],
                       [0, 1, 0],
                       [-np.sin(self.ori_shot[1]*np.pi/180), 0,
                        np.cos(self.ori_shot[1]*np.pi/180)]])
        rz = np.array([[np.cos(self.ori_shot[2]*np.pi/180), -np.sin(self.ori_shot[2]*np.pi/180), 0],
                       [np.sin(self.ori_shot[2]*np.pi/180), np.cos(self.ori_shot[2]*np.pi/180), 0],
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
        self.ori_shot_eucli = -Rotation.from_matrix(self.mat_rot_eucli).as_euler('xyz',
                                                                                 degrees=True)

    # pylint: disable-next=too-many-arguments too-many-locals
    def world_to_image(self, x_world: Union[np.array, float],
                       y_world: Union[np.array, float],
                       z_world: Union[np.array, float],
                       cam: Camera, dem: Dem, type_z: str = "a") -> np.array:
        """
        Calculates the c,l coordinates of a terrain point in an image.

        Args:
            x_world (Union[np.array, float]): the coordinate x of ground point.
            y_world (Union[np.array, float]): the coordinate y of ground point.
            z_world (Union[np.array, float]): the coordinate z of ground point.
            cam (Camera): the camera used.
            dem (Dem): Dem of the worksite.
            type_z (str): type of z, default = "a".
                          "h" height
                          "a" altitude / elevation
                          "al" altitude with linear alteration

        Returns:
            np.array: The image coordinate [c,l].
        """
        if type_z == "al" and dem is None:
            raise ValueError("Missing dem.")

        if isinstance(x_world, np.ndarray):
            dim = np.shape(x_world)
        else:
            dim = ()

        p_eucli = self.projeucli.world_to_euclidean(x_world, y_world, z_world)
        pos_eucli = np.copy(self.pos_shot_eucli)
        pos_eucli[2] = self.get_z_with_type(cam, dem, type_z)
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
    def image_to_world(self, col: Union[np.array, float], line: Union[np.array, float], cam: Camera,
                       dem: Dem, type_z: str) -> np.array:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            dem (Dem): Dem of the worksite.
            type_z (str): type of z, default = "a".
                          "h" height
                          "a" altitude / elevation
                          "al" altitude with linear alteration

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        if dem is None:
            raise ValueError("Missing dem.")

        if isinstance(col, np.ndarray):
            dim = np.shape(col)
        else:
            dim = ()

        z_world = np.full_like(col, dem.get(self.pos_shot[0], self.pos_shot[1]))
        x_world, y_world, _ = self.image_z_to_world(col, line, cam, dem, type_z, z_world)
        precision_reached = False
        nbr_iter = 0
        iter_max = 10
        while not precision_reached and nbr_iter < iter_max:
            z_world = dem.get(x_world, y_world)
            x_new_world, y_new_world, z_new_world = self.image_z_to_world(col, line, cam,
                                                                          dem, type_z, z_world)
            x_diff = (x_new_world - x_world) ** 2
            y_diff = (y_new_world - y_world) ** 2
            z_diff = (z_new_world - z_world) ** 2
            dist2 = x_diff + y_diff + z_diff
            precision_reached = np.any(dist2 < 0.01**2)
            x_world, y_world, z_world = x_new_world, y_new_world, z_new_world
            nbr_iter += 1

        x_world = change_dim(x_world, dim)
        y_world = change_dim(y_world, dim)
        z_world = change_dim(z_world, dim)
        return np.array([x_world, y_world, z_world])

    # pylint: disable-next=too-many-locals too-many-arguments
    def image_z_to_world(self, col: Union[np.array, float], line: Union[np.array, float],
                         cam: Camera, dem: Dem, type_z: str,
                         z: Union[np.array, float] = 0) -> np.array:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            dem (Dem): Dem of the worksite.
            type_z (str): type of z, default = "a".
                          "h" height
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
        pos_eucli = np.copy(self.pos_shot_eucli)
        pos_eucli[2] = self.get_z_with_type(cam, dem, type_z)
        p_local = self.mat_rot_eucli.T @ np.vstack([x_bundle, y_bundle, z_bundle])
        p_local = p_local + pos_eucli.reshape((3, 1))
        lamb = (z - pos_eucli[2])/(p_local[2] - pos_eucli[2])
        x_local = pos_eucli[0] + (p_local[0] - pos_eucli[0]) * lamb
        y_local = pos_eucli[1] + (p_local[1] - pos_eucli[1]) * lamb
        x_world, y_world, _ = self.projeucli.euclidean_to_world(x_local, y_local, z)
        return np.array([change_dim(x_world, dim), change_dim(y_world, dim), z])

    def image_to_bundle(self, col: Union[np.array, float],
                        line: Union[np.array, float], cam: Camera) -> np.array:
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

    def tranform_vertical(self) -> float:
        """
        Get new z position for the acquisition.
        It is a height z (altitude z).

        Args:
            projeucli (EuclideanProj): Eucliean system.

        Returns:
            float: New height z.
        """
        coor_geog = self.projeucli.proj_engine.tf.carto_to_geog(self.pos_shot[0],
                                                                self.pos_shot[1],
                                                                self.pos_shot[2])
        try:
            new_z = self.projeucli.proj_engine.tf.geog_to_geoid(coor_geog[0],
                                                                coor_geog[1],
                                                                coor_geog[2])[2]
        except AttributeError:
            new_z = None

        if new_z == np.inf:
            raise ValueError("out geoid")
        return new_z

    def get_z_with_type(self, cam: Camera, dem: Dem, type_z: str):
        """
        Transforms acquisition z into type.
        For the specific case of a z at altitude with linear weathering.
        To de-correct the z.

        Args:
            cam (Camera): The camera of the shot.
            dem (Dem): Dem of the worksite.
            type_z (str): Type of z.

        Returns:
            float: The right z for the type of data.
        """
        z_eucli = self.pos_shot_eucli[2]
        if type_z == "al":
            if dem.type_dem == "height":
                z = self.tranform_vertical()

            scale_factor = self.projeucli.proj_engine.get_scale_factor(self.pos_shot[0],
                                                                       self.pos_shot[1])
            z_nadir = self.image_to_world(cam.ppax, cam.ppay, cam, dem, "p")[2]
            z = (z + z_nadir * scale_factor) / (1 + scale_factor)
            z_eucli = self.projeucli.world_to_euclidean(self.pos_shot[0], self.pos_shot[1], z)[2]
        return z_eucli
