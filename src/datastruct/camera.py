"""
Camera data class module.
"""
from dataclasses import dataclass


@dataclass
class Camera:
    """
    Shot class definition.

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
    width: float = None
    height: float = None

    def add_dim_image(self, width: float, height: float) -> None:
        """
        Add shape of image, width height.

        Args:
            width (float): Width of the image.
            height (float): Height of the image.
        """
        self.width = width
        self.height = height
