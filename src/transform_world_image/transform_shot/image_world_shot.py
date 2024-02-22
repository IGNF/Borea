"""
Image world transformation module for Shot
"""
from typing import Union
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.dtm import Dtm
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data
from src.transform_world_image.transform_shot.conversion_coor_shot import conv_output_z_type
from src.utils.conversion import change_dim


class ImageWorldShot():
    """
    Function image_to_world for shot.
    """
    def __init__(self, shot: Shot) -> None:
        self.shot = shot

    # pylint: disable-next=too-many-locals too-many-arguments
    def image_to_world(self, col: Union[np.ndarray, float], line: Union[np.ndarray, float],
                       cam: Camera, type_z_data: str, type_z_shot: str,
                       nonadir: bool = True) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            type_z_data (str): type of z data you want in output, "height" or "altitude".
            type_z_shot (str): type of z shot, "height" or "altitude".
            nonadir (bool): To calculate nadir no take linear alteration.

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        if type_z_data != type_z_shot and not ProjEngine().geog_to_geoid:
            raise ValueError("Missing geoid")

        if not Dtm().path_dtm:
            raise ValueError("Missing dtm")

        if isinstance(col, np.ndarray):
            dim = np.shape(col)
        else:
            dim = ()

        z_world = np.full_like(col, Dtm().get_z_world(self.shot.pos_shot[0], self.shot.pos_shot[1]))
        x_world, y_world, _ = self.image_z_to_world(col, line, cam, type_z_shot, z_world, nonadir)
        precision_reached = False
        nbr_iter = 0
        iter_max = 10
        while not precision_reached and nbr_iter < iter_max:
            z_world = Dtm().get_z_world(x_world, y_world)
            x_new_world, y_new_world, z_new_world = self.image_z_to_world(col, line, cam,
                                                                          type_z_shot, z_world,
                                                                          nonadir)
            x_diff = (x_new_world - x_world) ** 2
            y_diff = (y_new_world - y_world) ** 2
            z_diff = (z_new_world - z_world) ** 2
            dist2 = x_diff + y_diff + z_diff
            precision_reached = np.any(dist2 < 0.01**2)
            x_world, y_world, z_world = x_new_world, y_new_world, z_new_world
            nbr_iter += 1

        x_world, y_world, z_world = conv_output_z_type(x_world, y_world, z_world,
                                                       Dtm().type_dtm, type_z_data)
        x_world = change_dim(x_world, dim)
        y_world = change_dim(y_world, dim)
        z_world = change_dim(z_world, dim)
        return np.array([x_world, y_world, z_world])

    # pylint: disable-next=too-many-locals too-many-arguments
    def image_z_to_world(self, col: Union[np.ndarray, float], line: Union[np.ndarray, float],
                         cam: Camera, type_z_shot: str,
                         z: Union[np.ndarray, float] = 0, nonadir: bool = True) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            col (Union[np.array, float]): Column coordinates of image point(s).
            line (Union[np.array, float]): Line coordinates of image point(s).
            cam (Camera): Objet cam which correspond to the shot.
            type_z_shot (str): type of z "height" or "altitude"
            z (Union[np.array, float]): La position z du point par défault = 0.
            nonadir (bool): To calculate nadir no take linear alteration.

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

        z_shot = conv_z_shot_to_z_data(self.shot, type_z_shot, Dtm().type_dtm, nonadir)

        pos_eucli = self.shot.projeucli.world_to_euclidean(self.shot.pos_shot[0],
                                                           self.shot.pos_shot[1],
                                                           z_shot)

        p_local = self.shot.mat_rot_eucli.T @ np.vstack([x_bundle, y_bundle, z_bundle])
        p_local = p_local + pos_eucli.reshape((3, 1))
        lamb = (z - pos_eucli[2])/(p_local[2] - pos_eucli[2])
        x_local = pos_eucli[0] + (p_local[0] - pos_eucli[0]) * lamb
        y_local = pos_eucli[1] + (p_local[1] - pos_eucli[1]) * lamb
        x_world, y_world, _ = self.shot.projeucli.euclidean_to_world(x_local, y_local, z)
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
        x_shot, y_shot, z_shot = self.shot.f_sys_inv(x_shot, y_shot, z_shot)
        x_bundle = x_shot / cam.focal * z_shot
        y_bundle = y_shot / cam.focal * z_shot
        z_bundle = z_shot
        return np.array([x_bundle, y_bundle, z_bundle])
