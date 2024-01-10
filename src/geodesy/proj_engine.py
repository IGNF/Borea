"""
Module for manipulating a cartographic system.
"""
from typing import Union, List
from dataclasses import dataclass
import pyproj
import numpy as np


@dataclass
class ProjEngine:
    """
    This class provides functions for using a cartographic system.

    Args:
        epsg (str): Code epsg of the porjection ex: "EPSG:2154".
    """
    epsg: str
    projection_list: dict = None

    def __post_init__(self) -> None:
        if self.projection_list is not None:
            self.crs = pyproj.CRS.from_string(self.epsg)
            self.crs_geoc = pyproj.CRS.from_string(self.projection_list["geoc"])
            self.crs_geog = pyproj.CRS.from_string(self.projection_list["geog"])
            self.proj = pyproj.Proj(self.crs)
            self.tf = Transform(self)

    def get_meridian_convergence(self, x_carto: Union[np.array, List[float], float],
                                 y_carto: Union[np.array, List[float], float]) -> float:
        """
            Compute meridian convergence.
            Values are extracted from pyproj.

            Args:
                x_carto (np.array, List[float], float): x cartographic coordinates.
                y_carto (np.array, List[float], float): y cartographic coordinates.

            Returns:
                np.array : meridian convergence in degree
        """
        # pylint: disable-next=unpacking-non-sequence
        (x_geog, y_geog) = self.tf.carto_to_geog(x_carto, y_carto)
        return -np.array(self.proj.get_factors(x_geog, y_geog).meridian_convergence)


@dataclass
class Transform():
    """
    This class provides functions to tranform coordinate system.

    Args:
        pe (ProjEngin): Tranformation for the ProjEgine.
    """
    pe: ProjEngine

    def __post_init__(self) -> None:
        # Transform cartographic coordinates to geographic coordinates
        self.carto_to_geog = pyproj.Transformer.from_crs(self.pe.crs, self.pe.crs_geog).transform
        # Transform geographic coordinates to cartographic coordinates
        self.geog_to_carto = pyproj.Transformer.from_crs(self.pe.crs_geog, self.pe.crs).transform
        # Transform cartographic coordinates to geocentric coordinates
        self.carto_to_geoc = pyproj.Transformer.from_crs(self.pe.crs, self.pe.crs_geoc).transform
        # Transform geocentric coordinates to cartographic coordinates
        self.geoc_to_carto = pyproj.Transformer.from_crs(self.pe.crs_geoc, self.pe.crs).transform
