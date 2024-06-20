"""
Camera data class module.
"""
from dataclasses import dataclass, field


@dataclass
class Camera:
    """
    Camera class definition.

    Args:
        name_camera (str): Name of the camera.
        ppax (float): Center of distortion in x.
        ppay (float): Center of distortion in y.
        focal (float): Focal of the camera.
        width (int): Width of the image in pixel.
        height (int): Height of the image in pixel.
    """
    name_camera: str
    ppax: float = field(default=None)
    ppay: float = field(default=None)
    focal: float = field(default=None)
    width: int = field(default=None)
    height: int = field(default=None)
