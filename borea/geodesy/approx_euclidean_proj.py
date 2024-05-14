"""
A module for manipulating an approximate euclidean projection.
"""
import numpy as np
from borea.geodesy.euclidean_proj import EuclideanProj


class ApproxEuclideanProj(EuclideanProj):
    """
     This class represents an approximate Euclidean projection system.

    Args:
        x_central (float): x coordinate of the central point of the Euclidean system.
        y_central (float): y coordinate of the central point of the Euclidean system.

    .. note::
        A Euclidean system is a local Euclidean reference system in which
        the collinear equation is valid.
    """
    def __init__(self, x_central: float, y_central: float) -> None:
        super().__init__(x_central, y_central)
        self.earth_raduis = 6366000

    def mat_to_mat_eucli(self, x: float, y: float, mat: np.ndarray) -> np.ndarray:
        """
        Transform the rotation matrix (World system) into rotation matrix (Euclidian systeme).

        Args:
            x (float): x coordinate of the point.
            y (float): y coordinate of the point.
            mat (np.array): Rotation matrix (World system).

        Returns:
            np.array: Euclidean rotation matrix.
        """
        _, _ = x, y
        return mat

    def mat_eucli_to_mat(self, x: float, y: float, mat_eucli: np.ndarray) -> np.ndarray:
        """
        Transform the rotation matrix (Euclidean system) into rotation matrix (World system).

        Args:
            x (float): x coordinate of the point.
            y (float): y coordinate of the point.
            mat_eucli (np.array): Rotation matrix (Euclidean system).

        Returns:
            np.array: Rotation matrix (World system).
        """
        _, _ = x, y
        return mat_eucli

    def world_to_eucli(self, coor_world: np.ndarray) -> np.ndarray:
        """
        Transform a point from the world coordinate reference system into
        the Euclidean coordinate reference system.

        Args:
            coor_world (np.array): World coordinate of the point [X, Y, Z].

        Returns:
            np.array: Point in the Euclidean coordinate reference system.
        """
        dx = coor_world[0] - self.pt_central[0]
        dy = coor_world[1] - self.pt_central[1]
        tt = (dx ** 2 + dy ** 2) / (4 * self.earth_raduis)
        cc = (self.earth_raduis + coor_world[2]) / (tt + self.earth_raduis)
        xe = dx * cc
        ye = dy * cc
        ze = ((self.earth_raduis - tt) * cc) - self.earth_raduis
        return np.array([xe, ye, ze])

    def eucli_to_world(self, coor_eucli: np.ndarray) -> np.ndarray:
        """
        Transform a point from the Euclidean coordinate reference system into
        the world coordinate reference system.

        Args:
            coor_eucli: Euclidean coordinate of the point [X, Y, Z].

        Returns:
            np.array: Point in the World coordinate reference system.
        """
        rz = self.earth_raduis + coor_eucli[2]
        rh = (rz**2 + coor_eucli[0]**2 + coor_eucli[1]**2)**0.5
        rz = (2*self.earth_raduis)/(rz + rh)
        x = self.pt_central[0] + (coor_eucli[0] * rz)
        y = self.pt_central[1] + (coor_eucli[1] * rz)
        z = rh - self.earth_raduis
        return np.array([x, y, z])
