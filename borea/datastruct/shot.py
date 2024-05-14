"""
Acquisition data class module.
"""
import numpy as np
from scipy.spatial.transform import Rotation as R
from borea.geodesy.proj_engine import ProjEngine
from borea.geodesy.approx_euclidean_proj import ApproxEuclideanProj
from borea.geodesy.local_euclidean_proj import LocalEuclideanProj
from borea.utils.check.check_order_axe import check_order_axe


# pylint: disable=too-many-instance-attributes too-many-arguments
class Shot:
    """
    Shot class definition.

    Args:
        name_shot (str): Name of the shot.
        pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
        ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa] in degree.
        name_cam (str): Name of the camera.
        unit_angle (str): Unit of angle 'degrees', 'radian'.
        linear_alteration (bool): True if z shot is correct of linear alteration.
        order_axe (str): Order of rotation matrix axes.
    """
    def __init__(self, name_shot: str, pos_shot: np.ndarray,
                 ori_shot: np.ndarray, name_cam: str,
                 unit_angle: str, linear_alteration: bool,
                 order_axe: str) -> None:
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.pos_shot_eucli = None
        self.linear_alteration = linear_alteration
        self.ori_shot = ori_shot
        self.unit_angle = unit_angle
        self.name_cam = name_cam
        self.order_axe = order_axe
        self.z_nadir = None
        self.co_points = {}
        self.gcp2d = {}
        self.gcp3d = {}
        self.mat_rot = self.set_rot_shot()
        self.mat_rot_eucli = None
        self.projeucli = None
        self.approxeucli = False
        self.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        self.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

    @classmethod
    def from_param_euclidean(cls, name_shot: str, pos_eucli: np.ndarray,
                             mat_ori_eucli: np.ndarray, name_cam: str,
                             unit_angle: str, linear_alteration: bool,
                             order_axe: str, approx: bool) -> None:
        """
        Construction of a shot object using the Euclidean position.

        Args:
            name_shot (str): Name of the shot.
            pos_eucli (np.array): Euclidean position of the shot.
            mat_ori_eucli (np.array): Euclidean rotation matrix of the shot.
            name_cam (str): Name of the camera.
            unit_angle (str): Unit of angle 'degrees', 'radian'.
            linear_alteration (bool): True if z shot is correct of linear alteration.
            order_axe (str): Order of rotation matrix axes.
            approx (bool): True if you want to use approx euclidean system.

        Returns:
            Shot: The shot.
        """
        shot = cls(name_shot, np.array([0, 0, 0]), np.array([0, 0, 0]),
                   name_cam, unit_angle, linear_alteration, order_axe)
        shot.pos_shot_eucli = pos_eucli
        shot.approxeucli = approx
        if approx:
            shot.projeucli = ApproxEuclideanProj(pos_eucli[0], pos_eucli[1])
        else:
            shot.projeucli = LocalEuclideanProj(pos_eucli[0], pos_eucli[1])
        unitori = shot.unit_angle == "degree"
        shot.pos_shot = shot.projeucli.eucli_to_world(pos_eucli)
        shot.co_points = {}
        shot.gcp3d = {}
        shot.gcp2d = {}
        shot.mat_rot = shot.projeucli.mat_eucli_to_mat(shot.pos_shot[0], shot.pos_shot[1],
                                                       mat_ori_eucli)
        shot.mat_rot_eucli = mat_ori_eucli
        order_xyz = check_order_axe(order_axe)
        shot.ori_shot = -(R.from_euler("x", np.pi) *
                          R.from_matrix(shot.mat_rot)).as_euler(order_xyz, degrees=unitori)

        shot.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        shot.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

        return shot

    def set_rot_shot(self) -> np.ndarray:
        """
        Build the rotation matrix with omega phi kappa.

        Returns:
            np.array: The rotation matrix.
        """
        order_xyz = check_order_axe(self.order_axe)
        rot = R.from_euler(order_xyz, -np.array(self.ori_shot), degrees=self.unit_angle == "degree")
        rot = R.from_euler("x", np.pi) * rot
        return rot.as_matrix()

    def set_param_eucli_shot(self, approx: bool) -> None:
        """
        Setting up Euclidean parameters projeucli, pos_shot_eucli, mat_rot_eucli.

        Args:
            approx (bool): True if you want to use approx euclidean system.
        """
        if approx:
            self.projeucli = ApproxEuclideanProj(self.pos_shot[0], self.pos_shot[1])
        else:
            self.projeucli = LocalEuclideanProj(self.pos_shot[0], self.pos_shot[1])

        self.mat_rot_eucli = self.projeucli.mat_to_mat_eucli(self.pos_shot[0],
                                                             self.pos_shot[1],
                                                             self.mat_rot)
        self.approxeucli = approx
        self.pos_shot_eucli = self.projeucli.world_to_eucli(self.pos_shot)

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

    def set_order_axe(self, order_axe: str) -> None:
        """
        Allows to change order of axe for the matrice and angle.

        Args:
            order_axe (str): New order axe.
        """
        if order_axe != self.order_axe:
            self.order_axe = order_axe
            order_xyz = check_order_axe(self.order_axe)
            unitori = self.unit_angle == "degree"
            self.ori_shot = -(R.from_euler("x", np.pi) *
                              R.from_matrix(self.mat_rot)).as_euler(order_xyz, degrees=unitori)

    def get_z_remove_scale_factor(self) -> float:
        """
        Return Z after removing the scale factor. The Z of the object is NOT modified.

        Returns:
            float: z without linear alteration.
        """
        if self.z_nadir:
            scale_factor = ProjEngine().get_scale_factor(self.pos_shot[0],
                                                         self.pos_shot[1])
            new_z = (self.pos_shot[2] + scale_factor * self.z_nadir) / (1 + scale_factor)
        else:
            raise ValueError(f"No removing linear alteration of the z shot {self.name_shot}, "
                             "because no dtm or no set z_nadir of shot. For setting z_nadir "
                             "of shots make dtm or add work.set_z_nadir_shot()")

        return new_z

    def get_z_add_scale_factor(self) -> float:
        """
        Return Z after adding the scale factor. The Z of the object is NOT modified.

        Returns:
            float: z with linear alteration.
        """
        if self.z_nadir:
            scale_factor = ProjEngine().get_scale_factor(self.pos_shot[0],
                                                         self.pos_shot[1])
            new_z = self.pos_shot[2] + scale_factor * (self.pos_shot[2] - self.z_nadir)
        else:
            raise ValueError(f"No adding linear alteration of the z shot {self.name_shot}, "
                             "because no dtm or no set z_nadir of shot. For setting z_nadir "
                             "of shots make dtm or add work.set_z_nadir_shot()")

        return new_z
