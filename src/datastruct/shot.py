"""
Acquisition data class module
"""
from dataclasses import dataclass, field
from src.datastruct.camera import Camera
import numpy as np


@dataclass
class Shot:
    """
    Shot class definition

    Args:
        name_shot (str): Name of the shot.
        pos_shot (numpy.array): Array of coordinate position [X, Y, Z].
        ori_shot (numpy.array): Array of orientation of the shot [Omega, Phi, Kappa].
        name_cam (str): Name of the camera.
    """
    name_shot: str
    pos_shot: np.array
    ori_shot: np.array
    name_cam: str
    copoints: dict = field(default_factory=dict)
    gcps: dict = field(default_factory=dict)
    mat_rot: np.array = field(init=False)

    def __post_init__(self) -> np.array:
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
        self.mat_rot = rx @ ry @ rz
    
    def world_to_image(self, point: np, cam: Camera) -> np:
        """
        Calculates the c,l coordinates of a terrain point in an image

        Args:
            point (np.array): the coordinateof ground point [x, y, z]
            cam (Camera): the camera used

        Returns:
            np.array: The image coordinate [c,l]
        """
        # TODO: manque le changement de projection conique en cartesien
        diff_p = point - self.pos_shot
        num_x = self.mat_rot[0, :] @ (diff_p)
        num_y = self.mat_rot[1, :] @ (diff_p)
        dem = self.mat_rot[2, :] @ (diff_p)
        x_col = cam.ppax - cam.focal * (num_x/dem)
        y_lig = cam.ppay - cam.focal * (num_y/dem)
        return np.array([x_col, y_lig])
