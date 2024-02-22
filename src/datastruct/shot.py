"""
Acquisition data class module.
"""
import numpy as np
from scipy.spatial.transform import Rotation
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


# pylint: disable=too-many-instance-attributes too-many-arguments
class Shot:
    """
    Shot class definition.

    Args:
        name_shot (str): Name of the shot.
        pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
        ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa] in degree.
        name_cam (str): Name of the camera.
        unit_angle (str): unit of angle 'degrees', 'radian'.
        linear_alteration (bool): True if z shot is correct of linear alteration.
    """
    def __init__(self, name_shot: str, pos_shot: np.ndarray,
                 ori_shot: np.ndarray, name_cam: str,
                 unit_angle: str, linear_alteration: bool) -> None:
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.pos_shot_eucli = None
        self.linear_alteration = linear_alteration
        self.ori_shot = ori_shot
        self.unit_angle = unit_angle
        self.name_cam = name_cam
        self.z_nadir = None
        self.copoints = {}
        self.gipoints = {}
        self.gcps = {}
        self.mat_rot = self.set_rot_shot()
        self.mat_rot_eucli = None
        self.projeucli = None
        self.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        self.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

    @classmethod
    def from_param_euclidean(cls, name_shot: str, pos_eucli: np.ndarray,
                             mat_ori_eucli: np.ndarray, name_cam: str,
                             unit_angle: str, linear_alteration: bool) -> None:
        """
        Construction of a shot object using the Euclidean position.

        Args:
            name_shot (str): Name of the shot.
            pos_eucli (np.array): Euclidean position of the shot.
            mat_ori_eucli (np.array): Euclidean rotation matrix of the shot.
            name_cam (str): Name of the camera.
            unit_angle (str): unit of angle 'degrees', 'radian'.
            linear_alteration (bool): True if z shot is correct of linear alteration.

        Returns:
            Shot: The shot.
        """
        shot = cls(name_shot, np.array([0, 0, 0]), np.array([0, 0, 0]),
                   name_cam, unit_angle, linear_alteration)
        shot.pos_shot_eucli = pos_eucli
        shot.projeucli = EuclideanProj(pos_eucli[0], pos_eucli[1])
        unitori = shot.unit_angle == "degree"
        shot.pos_shot = shot.projeucli.euclidean_to_world(pos_eucli)
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
        if self.unit_angle == "degree":
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

    def set_param_eucli_shot(self) -> None:
        """
        Setting up Euclidean parameters projeucli, pos_shot_eucli, mat_rot_eucli.
        """
        self.projeucli = EuclideanProj(self.pos_shot[0], self.pos_shot[1])
        self.pos_shot_eucli = self.projeucli.world_to_euclidean(self.pos_shot)
        self.mat_rot_eucli = self.projeucli.mat_to_mat_eucli(self.pos_shot[0],
                                                             self.pos_shot[1],
                                                             self.mat_rot)

    def set_z_nadir(self, z_nadir: float) -> None:
        """
        Give z nadir to the shot.

        Args:
            z_nadir (flaot): z_nadir of the shot.
        """
        self.z_nadir = z_nadir

    def set_unit_angle(self, unit_angle: str) -> None:
        """
        Allows you to change the orientation angle unit.

        Args:
            unit_angle (str): Unit angle.
        """
        if unit_angle != self.unit_angle:
            self.unit_angle = unit_angle
            if unit_angle == "radian":
                self.ori_shot = self.ori_shot*np.pi/180
            else:
                self.ori_shot = self.ori_shot*180/np.pi

    def set_type_z(self, type_z: str) -> None:
        """
        Allows you to change the type of z.

        Args:
            type_z (str): z type height or altitude.
        """
        if type_z == "height":
            self.pos_shot[2] = ProjEngine().tranform_height(self.pos_shot)
        else:
            self.pos_shot[2] = ProjEngine().tranform_altitude(self.pos_shot)

    def set_linear_alteration(self, linear_alteration: bool) -> None:
        """
        Allows you to correct or de-correct the linear alteration.

        Args:
            linear_alteration (bool): Linear alteration boolean.
        """
        if linear_alteration != self.linear_alteration:
            self.linear_alteration = linear_alteration
            if linear_alteration:
                self.pos_shot[2] = self.get_z_add_scale_factor()
            else:
                self.pos_shot[2] = self.get_z_remove_scale_factor()

    def get_z_remove_scale_factor(self) -> float:
        """
        Return Z after removing the scale factor. The Z of the object is NOT modified.

        Returns:
            float: z without linear alteration
        """
        scale_factor = ProjEngine().get_scale_factor(self.pos_shot[0],
                                                     self.pos_shot[1])
        return (self.pos_shot[2] + scale_factor * self.z_nadir) / (1 + scale_factor)

    def get_z_add_scale_factor(self) -> float:
        """
        Return Z after adding the scale factor. The Z of the object is NOT modified.

        Returns:
            float: z with linear alteration.
        """
        scale_factor = ProjEngine().get_scale_factor(self.pos_shot[0],
                                                     self.pos_shot[1])
        return self.pos_shot[2] + scale_factor * (self.pos_shot[2] - self.z_nadir)
