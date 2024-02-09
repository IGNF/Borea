"""
Module for manipulating a cartographic system.
"""
from os import path
from typing import Union, List
from dataclasses import dataclass
import pyproj
import numpy as np


@dataclass
# pylint: disable-next=too-many-instance-attributes
class ProjEngine:
    """
    This class provides functions for using a cartographic system.

    Args:
        epsg (str): Code epsg of the porjection ex: "EPSG:2154".
        projection_list (dict): Dictionnary of the projection json.
        path_geotiff (str): Path to the forlder of GeoTIFF.
    """
    epsg: str
    projection_list: dict = None
    path_geotiff: str = None

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
            np.array : Meridian convergence in degree.
        """
        # pylint: disable-next=unpacking-non-sequence
        (x_geog, y_geog) = self.tf.carto_to_geog(x_carto, y_carto)
        return -np.array(self.proj.get_factors(x_geog, y_geog).meridian_convergence)

    def get_scale_factor(self, x_carto: Union[np.array, List[float], float],
                         y_carto: Union[np.array, List[float], float]) -> np.array:
        """
        Compute scale factor.
        Values are extracted from pyproj.

        Args:
            x_carto (Union[np.array, List[float], float]): x cartographic coordinates.
            y_carto (Union[np.array, List[float], float]): y cartographic coordinates.

        Returns:
            np.array: Scale factor and meridian convergence.
        """
        # pylint: disable-next=unpacking-non-sequence
        x_geog, y_geog = self.tf.carto_to_geog(x_carto, y_carto)
        return np.array(self.proj.get_factors(x_geog, y_geog).meridional_scale) - 1


@dataclass
class Transform():
    """
    This class provides functions to tranform coordinate system.

    Args:
        pe (ProjEngin): Tranformation for the ProjEgine.
    """
    def __init__(self, pe: ProjEngine) -> None:
        # Transform cartographic coordinates to geographic coordinates
        self.carto_to_geog = pyproj.Transformer.from_crs(pe.crs, pe.crs_geog).transform
        # Transform geographic coordinates to cartographic coordinates
        self.geog_to_carto = pyproj.Transformer.from_crs(pe.crs_geog, pe.crs).transform
        # Transform cartographic coordinates to geocentric coordinates
        self.carto_to_geoc = pyproj.Transformer.from_crs(pe.crs, pe.crs_geoc).transform
        # Transform geocentric coordinates to cartographic coordinates
        self.geoc_to_carto = pyproj.Transformer.from_crs(pe.crs_geoc, pe.crs).transform

        if 'geoid' in pe.projection_list:
            self.tf_geoid(pe)

    def tf_geoid(self, pe: ProjEngine) -> None:
        """
        Create attribute transform, to transform geographic coordinates to geoide coordinates
        """
        if pe.path_geotiff is not None:
            ptiff = pe.path_geotiff
            geoid_list = [ptiff + geoid + '.tif' for geoid in pe.projection_list['geoid']]
            if not path.exists(geoid_list[0]):
                geoid_list = [geoid+'.tif' for geoid in pe.projection_list['geoid']]
        else:
            geoid_list = [geoid+'.tif' for geoid in pe.projection_list['geoid']]

        try:
            # Transform geographic coordinates to geoide coordinates
            self.geog_to_geoid = pyproj.Transformer.from_pipeline(f"+proj=vgridshift "
                                                                  f"+grids={','.join(geoid_list)} "
                                                                  "+multiplier=1").transform
            # Transform geoide coordinates to geographic coordinates
            self.geoid_to_geog = pyproj.Transformer.from_pipeline(f"+proj=vgridshift "
                                                                  f"+grids={','.join(geoid_list)} "
                                                                  "+multiplier=-1").transform
        except pyproj.exceptions.ProjError as e:
            raise pyproj.exceptions.ProjError(f"{geoid_list} The name of geotif is incorrect or "
                                              "does not exist in folder or "
                                              "in usr/share/proj !!!{e}") from e
