"""
Acquisition data class module
"""
import numpy as np
from src.datastruct.camera import Camera
from src.geodesy.euclidean_proj import EuclideanProj


# pylint: disable-next=too-many-instance-attributes
class Shot:
    """
    Shot class definition

    Args:
        name_shot (str): Name of the shot.
        pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
        ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa] in degree.
        name_cam (str): Name of the camera.
    """
    def __init__(self, name_shot: str, pos_shot: np, ori_shot: np, name_cam: str) -> None:
        self.name_shot = name_shot
        self.pos_shot = pos_shot
        self.ori_shot = ori_shot
        self.name_cam = name_cam
        self.copoints = {}
        self.gcps = {}
        self.mat_rot = self.set_rot_shot()
        self.f_sys = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)
        self.f_sys_inv = lambda x_shot, y_shot, z_shot: (x_shot, y_shot, z_shot)

    def set_rot_shot(self) -> np:
        """
        Build the rotation matrix with omega phi kappa
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

    def world_to_image(self, point: np, cam: Camera, projeucli: EuclideanProj) -> np:
        """
        Calculates the c,l coordinates of a terrain point in an image

        Args:
            point (np.array): the coordinateof ground point [x, y, z]
            cam (Camera): the camera used

        Returns:
            np.array: The image coordinate [c,l]
        """
        z_alti = self.tranform_vertical(projeucli)
        p_eucli = projeucli.world_to_euclidean(point[0], point[1], point[2])
        pos_eucli = projeucli.world_to_euclidean(self.pos_shot[0],
                                                 self.pos_shot[1],
                                                 z_alti)
        mat_eucli = projeucli.mat_to_mat_eucli(self.pos_shot[0], self.pos_shot[1], self.mat_rot)
        p_bundle = mat_eucli @ (p_eucli - pos_eucli)
        x_shot = p_bundle[0] * cam.focal / p_bundle[2]
        y_shot = p_bundle[1] * cam.focal / p_bundle[2]
        z_shot = p_bundle[2]
        x_shot, y_shot, z_shot = self.f_sys(x_shot, y_shot, z_shot)
        x_col = cam.ppax + x_shot
        y_lig = cam.ppay + y_shot
        return np.array([x_col, y_lig])

    # pylint: disable-next=too-many-locals too-many-arguments
    def image_to_world(self, col: float, line: float, cam: Camera,
                       projeucli: EuclideanProj, z: float = 0) -> np.array:
        """
        Calculate x and y cartographique coordinate with z = 0.

        Args:
            c (float): Column coordinates of image point(s).
            l (float): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            proj (EuclideanProj): Euclidean projection of the worksite.
            z (float): La position z du point par défault = 0.

        Returns:
            np.array: Cartographique coordinate [x,y,z]
        """
        x_bundle, y_bundle, z_bundle = self.image_to_bundle(col, line, cam)
        z_alti = self.tranform_vertical(projeucli)
        pos_eucli = projeucli.world_to_euclidean(self.pos_shot[0], self.pos_shot[1], z_alti)
        mat_eucli = projeucli.mat_to_mat_eucli(self.pos_shot[0], self.pos_shot[1], self.mat_rot)
        p_local = mat_eucli.T @ np.array([x_bundle, y_bundle, z_bundle])
        p_local = p_local + pos_eucli
        lamb = (z - pos_eucli[2])/(p_local[2] - pos_eucli[2])
        x_local = pos_eucli[0] + (p_local[0] - pos_eucli[0]) * lamb
        y_local = pos_eucli[1] + (p_local[1] - pos_eucli[1]) * lamb
        x_world, y_world, _ = projeucli.euclidean_to_world(x_local, y_local, z)
        return np.array([x_world, y_world, z])

    def image_to_bundle(self, col: float, line: float, cam: Camera) -> tuple:
        """
        Convert coordinate image col line to coordinate bundle

        Args:
            c (float): Column coordinates of image point(s).
            l (float): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.

        Returns:
            np.array: Cartographique coordinate [x,y,z]
        """
        x_shot = col - cam.ppax
        y_shot = line - cam.ppay
        z_shot = cam.focal
        x_shot, y_shot, z_shot = self.f_sys_inv(x_shot, y_shot, z_shot)
        x_bundle = x_shot / cam.focal * z_shot
        y_bundle = y_shot / cam.focal * z_shot
        z_bundle = z_shot
        return x_bundle, y_bundle, z_bundle

    def tranform_vertical(self, projeucli: EuclideanProj) -> float:
        """
        Get new z position for the acquisition.
        It is an elevation z

        Args:
            projeucli (EuclideanProj): Eucliean system

        Returns:
            float: new z elevation
        """
        coor_geog = projeucli.proj_engine.tf.carto_to_geog(self.pos_shot[0],
                                                           self.pos_shot[1],
                                                           self.pos_shot[2])
        try:
            new_z = projeucli.proj_engine.tf.geog_to_geoid(coor_geog[0],
                                                           coor_geog[1],
                                                           coor_geog[2])[2]
        except AttributeError as e:
            raise AttributeError("missing 'geoid' tag in projection.json or path to geotiff") from e

        if new_z == np.inf:
            raise ValueError("out geoid")
        return new_z
