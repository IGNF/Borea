"""
Camera data class module.
"""
from dataclasses import dataclass, field


@dataclass
class Camera:
    """
    Shot class definition.

    Args:
        name_camera (str): Name of the camera.
        ppax (float): Center of distortion in x.
        ppay (float): Center of distortion in y.
        focal (float): Focal of the camera.
        width (int): Width of the image in pixel.
        height (int): Height of the image in pixel.
    """
    name_camera: str
    ppax: float
    ppay: float
    focal: float
    width: int
    height: int
    pixel_size: float = field(default=None)
