"""
A module for manipulating a local euclidean projection.
"""
import numpy as np
from scipy.spatial.transform import Rotation as R
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj
from src.utils.check.check_array import check_array_transfo
from src.utils.change_dim import change_dim


class LocalEuclideanProj(EuclideanProj):
    """
    This class represents a Euclidean projection system.

    Args:
        x_central (float): x coordinate of the central point of the Euclidean system.
        y_central (float): y coordinate of the central point of the Euclidean system.

    .. note::
        A Euclidean system is a local Euclidean reference system in which
        the collinear equation is valid.
        The cartographic system parameters must be known.
    """
    def __init__(self, x_central: float, y_central: float) -> None:
        super().__init__(x_central, y_central)
        self.rot_to_euclidean_local = self.mat_rot_euclidean_local(x_central, y_central)

    def mat_rot_euclidean_local(self, x: float, y: float) -> np.ndarray:
        """
        Compute the transition matrix between the world system and
        the Euclidean system centred on a point.

        Args:
            x (float): x coordinate of the central point of the Euclidean system.
            y (float): y coordinate of the central point of the Euclidean system.

        Returns:
            np.array: Transition matrix.
        """
        lon, lat = ProjEngine().carto_to_geog(x, y)
        gamma = ProjEngine().get_meridian_convergence(x, y)

        # Matrix for switching to local cartesian coordinates
        rot_ecef_to_eucli = R.from_euler("ZYZ", np.array([lon, 90 - lat, 90 + gamma]),
                                         degrees=True).inv()
        return rot_ecef_to_eucli.as_matrix()

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
        # We are in the projection system, we pass into the local tangeant system
        matecef_to_rtl = self.mat_rot_euclidean_local(x, y)
        mat_eucli = mat @ matecef_to_rtl @ self.rot_to_euclidean_local.T
        return mat_eucli

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
        # We're in the local tangeant frame, now we're in the projection frame
        matecef_to_rtl = self.mat_rot_euclidean_local(x, y)
        mat = mat_eucli @ self.rot_to_euclidean_local @ matecef_to_rtl.T
        return mat

    def world_to_eucli(self, coor: np.ndarray) -> np.ndarray:
        """
        Transform a point from the world coordinate reference system into
        the Euclidean coordinate reference system.

        Args:
            coor (np.ndarray): Coordinate [X, Y, Z].

        Returns:
            np.array: x, y, z in the Euclidean coordinate reference system.
        """
        if isinstance(coor[0], np.ndarray):
            dim = np.shape(coor[0])
        else:
            dim = ()

        coor = check_array_transfo(coor[0], coor[1], coor[2])

        coor_geoc = np.array(ProjEngine().carto_to_geoc(coor[0], coor[1], coor[2]))
        central_geoc = np.array(ProjEngine().carto_to_geoc(self.pt_central[0],
                                                           self.pt_central[1],
                                                           self.pt_central[2]))
        dr = np.vstack([coor_geoc[0] - central_geoc[0],
                        coor_geoc[1] - central_geoc[1],
                        coor_geoc[2] - central_geoc[2]])
        point_eucli = (self.rot_to_euclidean_local @ dr) + np.array([self.pt_central]).T
        x_r = change_dim(np.array([point_eucli[0]]), dim)
        y_r = change_dim(np.array([point_eucli[1]]), dim)
        z_r = change_dim(np.array([point_eucli[2]]), dim)
        return np.array([x_r, y_r, z_r])

    def eucli_to_world(self, coor: np.ndarray) -> np.ndarray:
        """
        Transform a point from the Euclidean coordinate reference system into
        the world coordinate reference system.

        Args:
            coor (np.ndarray): Coordinate [X, Y, Z].

        Returns:
            np.array: x, y, z in the world coordinate reference system.
        """
        if isinstance(coor[0], np.ndarray):
            dim = np.shape(coor[0])
        else:
            dim = ()

        central_geoc = np.array(ProjEngine().carto_to_geoc(self.pt_central[0],
                                                           self.pt_central[1],
                                                           self.pt_central[2]))
        dr = np.vstack([coor[0] - self.pt_central[0],
                        coor[1] - self.pt_central[1],
                        coor[2] - self.pt_central[2]])
        point_geoc = (self.rot_to_euclidean_local.T @ dr) + np.array([central_geoc]).T
        x_gc, y_gc, z_gc = check_array_transfo(point_geoc[0], point_geoc[1], point_geoc[2])
        tup = ProjEngine().geoc_to_carto(x_gc, y_gc, z_gc)
        x_r = change_dim(np.array([tup[0]]), dim)
        y_r = change_dim(np.array([tup[1]]), dim)
        z_r = change_dim(np.array([tup[2]]), dim)
        return np.array([x_r, y_r, z_r])
