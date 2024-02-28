"""
Module for manipulating a cartographic system.
"""
from pathlib import Path
from typing import Union, List
from dataclasses import dataclass
import pyproj
import numpy as np
from src.geodesy.transform_geodesy import TransformGeodesy
from src.utils.singleton.singleton import Singleton


# pylint: disable=unpacking-non-sequence
@dataclass
class ProjEngine(TransformGeodesy, metaclass=Singleton):
    """
    This class provides functions for using a cartographic system.
    """
    epsg: int = None
    projection_list: dict = None
    path_geoid: Path = None

    def __post_init__(self) -> None:
        if self.projection_list is not None:
            self.crs = pyproj.CRS.from_epsg(self.epsg)
            self.proj = pyproj.Proj(self.crs)
            TransformGeodesy.__tf_init__(self, self.projection_list, self.path_geoid, self.crs)

    def set_epsg(self, epsg: int, proj_list: dict = None, path_geoid: Path = None) -> None:
        """
        Setter of the class ProjEngine.
        Allows to init the class with data.

        Args:
            epsg (int): Code epsg of the porjection ex: "EPSG:2154".
            projection_list (dict): Dictionnary of the projection json.
            path_geoid (Path): Path to the forlder of GeoTIFF.
        """
        self.epsg = epsg
        self.projection_list = proj_list
        self.path_geoid = path_geoid
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
        (x_geog, y_geog) = self.carto_to_geog(x_carto, y_carto)
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
        x_geog, y_geog = self.carto_to_geog(x_carto, y_carto)
        return np.array(self.proj.get_factors(x_geog, y_geog).meridional_scale) - 1
