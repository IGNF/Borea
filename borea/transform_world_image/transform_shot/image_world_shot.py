"""
Image world transformation module for Shot
"""
import numpy as np
from borea.datastruct.shot import Shot
from borea.datastruct.camera import Camera
from borea.datastruct.dtm import Dtm
from borea.geodesy.proj_engine import ProjEngine
from borea.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data
from borea.transform_world_image.transform_shot.conversion_coor_shot import conv_output_z_type


class ImageWorldShot():
    """
    Function image_to_world for shot.

    Args:
        shot (Shot): The shot for convert coordinate.
        cam (Camera): The camera of the shot.
    """
    def __init__(self, shot: Shot, cam: Camera) -> None:
        self.shot = shot
        self.cam = cam

    def image_to_world(self, img_coor: np.ndarray,
                       type_z_data: str, type_z_shot: str,
                       nonadir: bool = True) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            img_coor (np.array): Image coordinate [col line].
            type_z_data (str): Type of z data you want in output, "height" or "altitude".
            type_z_shot (str): Type of z shot, "height" or "altitude".
            nonadir (bool): To calculate nadir no take linear alteration.

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        if type_z_data != type_z_shot and not ProjEngine().geog_to_geoid:
            raise ValueError("Missing geoid")

        if not Dtm().path_dtm:
            raise ValueError("Missing dtm")

        img_coor = np.squeeze(img_coor)
        coor_world = self.image_world_iter(img_coor, type_z_shot, nonadir)

        coor_world = conv_output_z_type(coor_world, Dtm().type_dtm, type_z_data)

        return coor_world

    def image_world_iter(self, img_coor: np.ndarray,
                         type_z_shot: str, nonadir: bool = True) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            img_coor (np.array): Image coordinate [col line].
            type_z_shot (str): Type of z shot, "height" or "altitude".
            nonadir (bool): To calculate nadir no take linear alteration.

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        z_world = np.full_like(img_coor[0], Dtm().get_z_world(self.shot.pos_shot[0:2]))
        coor_world = self.image_z_to_world(img_coor, type_z_shot, z_world, nonadir)
        precision_reached = False
        nbr_iter = 0
        iter_max = 10
        while not precision_reached and nbr_iter < iter_max:
            z_world = np.squeeze(Dtm().get_z_world(coor_world[0:2]))
            coor_new_world = self.image_z_to_world(img_coor, type_z_shot, z_world, nonadir)
            x_diff = (coor_new_world[0] - coor_world[0]) ** 2
            y_diff = (coor_new_world[1] - coor_world[1]) ** 2
            z_diff = (coor_new_world[2] - coor_world[2]) ** 2
            dist2 = x_diff + y_diff + z_diff
            precision_reached = np.any(dist2 < 0.01**2)
            coor_world = coor_new_world
            nbr_iter += 1

        return coor_world

    def image_z_to_world(self, img_coor: np.ndarray, type_z_shot: str,
                         z: np.ndarray = 0, nonadir: bool = True) -> np.ndarray:
        """
        Calculate x and y cartographique coordinate with z.

        Args:
            img_coor (np.array): Image coordinate [col line].
            type_z_shot (str): Type of z "height" or "altitude".
            z (Union[np.array, float]): La position z du point par défault = 0.
            nonadir (bool): To calculate nadir no take linear alteration.

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        if isinstance(img_coor[0], np.ndarray):
            if np.all(z == 0):
                z = np.full_like(img_coor[0], 0)

        pt_bundle = self.image_to_bundle(img_coor)

        pos_shot_new_z = conv_z_shot_to_z_data(self.shot, type_z_shot, Dtm().type_dtm,
                                               nonadir, self.shot.approxeucli)

        pos_eucli = self.shot.projeucli.world_to_eucli(pos_shot_new_z)

        pt_eucli = self.local_to_eucli(pt_bundle, pos_eucli, z)

        pt_world = self.shot.projeucli.eucli_to_world(pt_eucli)
        np.array([pt_world[0], pt_world[1], z])

        return np.array([pt_world[0], pt_world[1], z])

    def image_to_bundle(self, img_coor: np.ndarray) -> np.ndarray:
        """
        Convert coordinate image col line to coordinate bundle.

        Args:
            img_coor (np.array): Image coordinate [col line].

        Returns:
            np.array: Cartographique coordinate [x,y,z].
        """
        x_shot = img_coor[0] - self.cam.ppax
        y_shot = img_coor[1] - self.cam.ppay
        z_shot = np.full_like(x_shot, self.cam.focal)
        x_shot, y_shot, z_shot = self.shot.f_sys_inv(x_shot, y_shot, z_shot)
        x_bundle = x_shot / self.cam.focal * z_shot
        y_bundle = y_shot / self.cam.focal * z_shot
        z_bundle = z_shot
        return np.array([x_bundle, y_bundle, z_bundle])

    def local_to_eucli(self, pt_bundle: np.ndarray, pos_eucli: np.ndarray,
                       z: np.ndarray) -> np.ndarray:
        """
        Convert coordinate point in local system to euclidean system.

        Args:
            pt_bundle (np.array): Point to convert [X, Y, Z].
            pos_eucli (np.array): Shot position in the euclidean system.
            z (np.array): Z position of points.

        Returns:
            np.array: [X, Y, Z] in euclidean system.
        """
        p_local = self.shot.mat_rot_eucli.T @ np.vstack(pt_bundle)
        p_local = np.squeeze(p_local + pos_eucli.reshape((3, 1)))
        lamb = (z - pos_eucli[2])/(p_local[2] - pos_eucli[2])
        x_local = pos_eucli[0] + (p_local[0] - pos_eucli[0]) * lamb
        y_local = pos_eucli[1] + (p_local[1] - pos_eucli[1]) * lamb
        return np.array([x_local, y_local, z])
