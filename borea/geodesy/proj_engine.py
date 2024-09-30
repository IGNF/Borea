"""
Module for manipulating a cartographic system.
"""
from typing import Union, List
from dataclasses import dataclass
import pyproj
import numpy as np
from borea.geodesy.transform_geodesy import TransformGeodesy
from borea.utils.singleton.singleton import Singleton


# pylint: disable=unpacking-non-sequence
@dataclass
class ProjEngine(metaclass=Singleton):
    """
    This class provides functions for using a cartographic system.
    """
    epsg: int = None
    geoid: list = None
    epsg_output: int = None

    def __post_init__(self) -> None:
        if self.epsg:
            self.crs = pyproj.CRS.from_epsg(self.epsg[0])
            self.proj = pyproj.Proj(self.crs)
            self.tf = TransformGeodesy(self.epsg, self.geoid, self.epsg_output)

    def set_epsg(self, epsg: list, geoid: list = None, epsg_output: int = None) -> None:
        """
        Setter of the class ProjEngine.
        Allows to init the class with data.

        Args:
            epsg (list): Code epsg of the projection ex: [2154].
            geoid (list): List of geoid to use.
            epsg_output (int): Code epsg of the output projection. If you want to change.
        """
        self.epsg = epsg
        self.geoid = geoid
        self.epsg_output = epsg_output
        self.__post_init__()

    def get_meridian_convergence(self, x_carto: Union[np.ndarray, List[float], float],
                                 y_carto: Union[np.ndarray, List[float], float]) -> np.ndarray:
        """
        Compute meridian convergence.
        Values are extracted from pyproj.

        Args:
            x_carto (np.array, List[float], float): x cartographic coordinates.
            y_carto (np.array, List[float], float): y cartographic coordinates.

        Returns:
            np.array : Meridian convergence in degree.
        """
        (x_geog, y_geog) = self.tf.carto_to_geog(x_carto, y_carto)
        return -np.array(self.proj.get_factors(x_geog, y_geog).meridian_convergence)

    def get_scale_factor(self, x_carto: Union[np.ndarray, List[float], float],
                         y_carto: Union[np.ndarray, List[float], float]) -> np.ndarray:
        """
        Compute scale factor.
        Values are extracted from pyproj.

        Args:
            x_carto (Union[np.array, List[float], float]): x cartographic coordinates.
            y_carto (Union[np.array, List[float], float]): y cartographic coordinates.

        Returns:
            np.array: Scale factor and meridian convergence.
        """
        x_geog, y_geog = self.tf.carto_to_geog(x_carto, y_carto)
        return np.array(self.proj.get_factors(x_geog, y_geog).meridional_scale) - 1
