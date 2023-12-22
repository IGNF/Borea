"""
Camera data class module
"""
from dataclasses import dataclass


@dataclass
class Camera:
    """
    Shot class definition

    Args:
        name_camera (str): Name of the camera.
        ppax (float): Center of distortion in x.
        ppay (float): Center of distortion in y.
        focal (float): Focal of the camera.
    """
    name_camera: str
    ppax: float
    ppay: float
    focal: float
