"""
World image transformation module for self
"""
import numpy as np


class WorldImageDtm:
    """
    Function world_to_image and image_to_world for dtm.
    Class parent of dtm.
    """
    def __init__(self, gt: tuple) -> None:
        self.gt = gt

    def image_to_world(self, coor_img: np.ndarray) -> np.ndarray:
        """
        Compute world coordinates from image coordinates.

        Args:
            coor_img (np.array): Coordinate image [column, line].

        Returns:
            np.array: x, y world coordinates.
        """
        if self.gt:
            x = (np.array(coor_img[0])+0.5) * self.gt[1] + self.gt[0]
            y = (np.array(coor_img[1])+0.5) * self.gt[5] + self.gt[3]
        else:
            x, y = np.nan, np.nan
        return np.array([x, y])

    def world_to_image(self, coor_world: np.ndarray) -> np.ndarray:
        """
        Compute image coordinates from world coordinates.

        Args:
            coor_world (np.array): Coordinate world 2D [X, Y].

        Returns:
            np.array: Image coordinates.
        """
        if self.gt:
            col = (np.array(coor_world[0]) - self.gt[0])/self.gt[1] - 0.5
            line = (np.array(coor_world[1]) - self.gt[3])/self.gt[5] - 0.5
        else:
            col, line = np.nan, np.nan
        return np.array([col, line])
