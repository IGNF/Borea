"""
World image transformation module for Shot
"""
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.dtm import Dtm
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data
from src.utils.change_dim import change_dim


class WorldImageShot():
    """
    Function world_to_image for shot.

    Args:
        shot (Shot): The shot for convert coordinate
        cam (Camera): The camera of the shot.
    """
    def __init__(self, shot: Shot, cam: Camera) -> None:
        self.shot = shot
        self.cam = cam

    def world_to_image(self, coor_world: np.ndarray,
                       type_z_data: str, type_z_shot: str) -> np.ndarray:
        """
        Calculates the c,l coordinates of a terrain point in an image.

        Args:
            coor_world (np.array): The coordinate [x, y, z] of ground point.
            type_z_data (str): Type of z of data, "height" or "altitude".
            type_z_shot (str): Type of z of worksite, "height" or "altitude".

        Returns:
            np.array: The image coordinate [c,l].
        """
        if type_z_data != type_z_shot and not ProjEngine().geog_to_geoid:
            raise ValueError("Missing geoid")

        if self.shot.linear_alteration and not Dtm().path_dtm:
            raise ValueError("Missing dtm")

        if isinstance(coor_world[0], np.ndarray):
            dim = np.shape(coor_world[0])
        else:
            dim = ()

        pos_shot_new_z = conv_z_shot_to_z_data(self.shot, type_z_shot, type_z_data)

        # Convert coordinate in world system to euclidean system
        p_eucli = self.shot.projeucli.world_to_euclidean(coor_world)
        pos_eucli = self.shot.projeucli.world_to_euclidean(pos_shot_new_z)

        # Convert coordinate in euclidean system to bundle system
        p_bundle = self.shot.mat_rot_eucli @ np.vstack([p_eucli[0] - pos_eucli[0],
                                                        p_eucli[1] - pos_eucli[1],
                                                        p_eucli[2] - pos_eucli[2]])

        # Convert coordinate in bundle system to image system
        x_col, y_line = self.bundle_to_image(p_bundle)

        return np.array([change_dim(x_col, dim), change_dim(y_line, dim)])

    def bundle_to_image(self, p_bundle: np.ndarray) -> tuple:
        """
        Convert coordinate bundle to coordinate image col line.

        Args:
            p_bundle (np.array): [X, Y, Z] coordinates in bundle.

        Returns:
            tuple: Image coordinate x_col y_line.
        """
        x_shot = p_bundle[0] * self.cam.focal / p_bundle[2]
        y_shot = p_bundle[1] * self.cam.focal / p_bundle[2]
        z_shot = p_bundle[2]
        x_shot, y_shot, z_shot = self.shot.f_sys(x_shot, y_shot, z_shot)
        x_col = self.cam.ppax + x_shot
        y_line = self.cam.ppay + y_shot

        return x_col, y_line
