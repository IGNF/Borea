"""
A module for manipulating an euclidean projection.
"""
import math as m
import numpy as np
from typing import Union
from src.geodesy.proj_engine import ProjEngine
from src.utils.conversion import check_array_transfo, change_dim


class EuclideanProj:
    """
    This class represents a Euclidean projection system.

    Args:
        x_central (float): x coordinate of the central point of the Euclidean system
        y_central (float): y coordinate of the central point of the Euclidean system
        proj_engine (ProjEngine): kernel of geodesy calculation

    .. note::
        A Euclidean system is a local Euclidean reference system in which
        the collinear equation is valid.
        The cartographic system parameters must be known.
    """
    def __init__(self, x_central: float, y_central: float, proj_engine: ProjEngine) -> None:
        self.x_central = x_central
        self.y_central = y_central
        self.z_central = 0
        self.proj_engine = proj_engine
        self.rot_to_euclidean_local = self.mat_rot_euclidean_local(self.x_central, self.y_central)

    def mat_rot_euclidean_local(self, x: float, y: float) -> np.array:
        """
        Compute the transition matrix between the world system and
        the Euclidean system centred on a point.

        Args:
            x (float): x coordinate of the central point of the Euclidean system
            y (float): y coordinate of the central point of the Euclidean system

        Returns:
            np.array: transition matrix
        """
        lon, lat = self.proj_engine.tf.carto_to_geog(x, y)
        gamma = self.proj_engine.get_meridian_convergence(x, y)

        # Matrice de passage en coordonnees cartesiennes locales
        sl = m.sin(lon * m.pi/180)
        sp = m.sin(lat * m.pi/180)
        sg = m.sin(gamma * m.pi/180)
        cl = m.cos(lon * m.pi/180)
        cp = m.cos(lat * m.pi/180)
        cg = m.cos(gamma * m.pi/180)
        rot_to_euclidean_local = np.zeros((3, 3))
        rot_to_euclidean_local[0, 0] = -cg * sl - sg * sp * cl
        rot_to_euclidean_local[0, 1] = cg * cl - sg * sp * sl
        rot_to_euclidean_local[0, 2] = sg * cp
        rot_to_euclidean_local[1, 0] = sg * sl - cg * sp * cl
        rot_to_euclidean_local[1, 1] = -sg * cl - cg * sp * sl
        rot_to_euclidean_local[1, 2] = cg * cp
        rot_to_euclidean_local[2, 0] = cp * cl
        rot_to_euclidean_local[2, 1] = cp * sl
        rot_to_euclidean_local[2, 2] = sp
        return rot_to_euclidean_local

    def mat_to_mat_eucli(self, x: float, y: float, mat: np.array) -> np.array:
        """
        Transform the rotation matrix (World system) into rotation matrix (Euclidian systeme)

        Args:
            x (float): x coordinate of the point
            y (float): y coordinate of the point
            mat (np.array): rotation matrix (World system)

        Returns:
            np.array: rotation matrix
        """

        # *-1 on two last line
        mat = mat*np.array([1, -1, -1]).reshape(-1, 1)

        # We are in the projection system, we pass into the local tangeant system
        matecef_to_rtl = self.mat_rot_euclidean_local(x, y)
        mat_eucli = mat @ matecef_to_rtl @ self.rot_to_euclidean_local.T
        return mat_eucli

    def world_to_euclidean(self, x: Union[np.array, float],
                           y: Union[np.array, float], z: Union[np.array, float]) -> np.array:
        """
        Transform a point from the world coordinate reference system into
        the Euclidean coordinate reference system.

        Args:
            x (Union[np.array, float]): x coordinate of the point
            y (Union[np.array, float]): y coordinate of the point
            z (Union[np.array, float]): z coordinate of the point

        Returns:
            np.array: x, y, z in the Euclidean coordinate reference system, dim = [[],[],[]]
        """
        if isinstance(x, np.ndarray):
            dim = np.shape(x)
        else:
            dim = ()

        x, y, z = check_array_transfo(x, y, z)

        x_geoc, y_geoc, z_geoc = self.proj_engine.tf.carto_to_geoc(x, y, z)
        central_geoc = self.proj_engine.tf.carto_to_geoc(self.x_central,
                                                         self.y_central,
                                                         self.z_central)
        dr = np.vstack([x_geoc-central_geoc[0], y_geoc-central_geoc[1], z_geoc-central_geoc[2]])
        point_eucli = (self.rot_to_euclidean_local @ dr) + np.array([[self.x_central,
                                                                      self.y_central,
                                                                      self.z_central]]).T
        x_r, y_r, z_r = check_array_transfo(point_eucli[0], point_eucli[1], point_eucli[2])
        x_r = change_dim(x_r, dim)
        y_r = change_dim(y_r, dim)
        z_r = change_dim(z_r, dim)
        return np.array([x_r, y_r, z_r])

    def euclidean_to_world(self, x: Union[np.array, float],
                           y: Union[np.array, float], z: Union[np.array, float]) -> np.array:
        """
        Transform a point from the Euclidean coordinate reference system into
        the world coordinate reference system.

        Args:
            x_eucli (Union[np.array, float]): x coordinate of the point
            y_eucli (Union[np.array, float]): y coordinate of the point
            z_eucli (Union[np.array, float]): y coordinate of the point

        Returns:
            np.array: x, y, z in the world coordinate reference system.
        """
        if isinstance(x, np.ndarray):
            dim = np.shape(x)
        else:
            dim = ()

        central_geoc = self.proj_engine.tf.carto_to_geoc(self.x_central,
                                                         self.y_central,
                                                         self.z_central)
        dr = np.vstack([x - self.x_central, y - self.y_central, z - self.z_central])
        point_geoc = (self.rot_to_euclidean_local.T @ dr) + np.array([[central_geoc[0],
                                                                       central_geoc[1],
                                                                       central_geoc[2]]]).T
        x_gc, y_gc, z_gc = check_array_transfo(point_geoc[0,:], point_geoc[1,:], point_geoc[2,:])
        tup = self.proj_engine.tf.geoc_to_carto(x_gc, y_gc, z_gc)
        x_r = change_dim(tup[0], dim)
        y_r = change_dim(tup[1], dim)
        z_r = change_dim(tup[2], dim)
        return np.array([x_r, y_r, z_r])
