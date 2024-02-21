"""
World image transformation module for self
"""
from typing import Union, Tuple, Any
import numpy as np


class WorldImageDtm:
    """
    Function world_to_image and image_to_world for dtm.
    Class parent of dtm.
    """
    def __init__(self, gt: tuple) -> None:
        self.gt = gt

    def image_to_world(self, c: Union[int, float, list, np.ndarray],
                       l: Union[int, float, list, np.ndarray]) -> Tuple[Any, Any]:
        """
        Compute world coordinates from image coordinates.

        Args:
            c (Union[int, float, list, np.ndarray]): Column coordinates.
            l (Union[int, float, list, np.ndarray]): Line coordinates.

        Returns:
            Tuple[Any, Any]: x, y world coordinates.
        """
        if self.gt:
            x = (np.array(c)+0.5) * self.gt[1] + self.gt[0]
            y = (np.array(l)+0.5) * self.gt[5] + self.gt[3]
        else:
            x, y = np.nan, np.nan
        return x, y

    def world_to_image(self, x: Union[int, float, list, np.ndarray],
                       y: Union[int, float, list, np.ndarray]) -> Tuple[Any, Any]:
        """
        Compute image coordinates from world coordinates.

        Args:
            x (Union[int, float, list, np.ndarray]): x world coordinate.
            y (Union[int, float, list, np.ndarray]): y world coordinate.

        Returns:
            Tuple[Any, Any]: Image coordinates.
        """
        if self.gt:
            col = (np.array(x) - self.gt[0])/self.gt[1] - 0.5
            line = (np.array(y) - self.gt[3])/self.gt[5] - 0.5
        else:
            col, line = np.nan, np.nan
        return col, line
