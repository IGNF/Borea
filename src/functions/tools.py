"""
Tool script with different functions:
- the image function : func_img()
"""
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera


def func_img(point: np, shot: Shot, cam: Camera) -> np:
    """
    Calculates the c,l coordinates of a terrain point in an image

    Args:
        point (np.array): the coordinateof ground point [x, y, z]
        shot (Shot): the shot where the image coordinate will be calculated
        cam (Camera): the camera used

    Returns:
        np.array: The image coordinate [c,l]
    """
    diff_p = point - shot.pos_shot
    num_x = shot.mat_rot[0, :] @ (diff_p)
    num_y = shot.mat_rot[1, :] @ (diff_p)
    dem = shot.mat_rot[2, :] @ (diff_p)
    x_col = cam.ppax - cam.focal * (num_x/dem)
    y_lig = cam.ppay - cam.focal * (num_y/dem)
    return np.array([x_col, y_lig])
