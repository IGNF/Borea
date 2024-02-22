"""
Module for class ProjEngine, transform geodesy
"""
from os import path
from pathlib import Path
from dataclasses import dataclass
from typing import Union
import pyproj
import numpy as np


# pylint: disable=unsubscriptable-object
@dataclass
class TransformGeodesy():
    """
    This class provides functions to tranform coordinate system.

    Args:
        projection_list (dict): Dictionnary of the projection json.
        path_geoid (Path): Path to the forlder of GeoTIFF.
        crs (pyproj): crs pyproj of the worksite.
    """
    carto_to_geoc = None
    geoc_to_carto = None
    carto_to_geog = None
    geog_to_carto = None
    geog_to_geoid = None
    geoid_to_geog = None

    def __tf_init__(self, projection_list: dict,
                    path_geoid: Path, crs: pyproj) -> None:
        crs_geoc = pyproj.CRS.from_string(projection_list["geoc"])
        crs_geog = pyproj.CRS.from_string(projection_list["geog"])
        # Transform cartographic coordinates to geographic coordinates
        self.carto_to_geog = pyproj.Transformer.from_crs(crs, crs_geog).transform
        # Transform geographic coordinates to cartographic coordinates
        self.geog_to_carto = pyproj.Transformer.from_crs(crs_geog, crs).transform
        # Transform cartographic coordinates to geocentric coordinates
        self.carto_to_geoc = pyproj.Transformer.from_crs(crs, crs_geoc).transform
        # Transform geocentric coordinates to cartographic coordinates
        self.geoc_to_carto = pyproj.Transformer.from_crs(crs_geoc, crs).transform

        if 'geoid' in projection_list:
            self.tf_geoid(projection_list, path_geoid)

    def tf_geoid(self, projection_list: dict, path_geoid: Path) -> None:
        """
        Create attribute transform, to transform geographic coordinates to geoide coordinates

        Args:
            projection_list (dict): Dictionnary of the projection json.
            path_geotiff (Path): Path to the forlder of GeoTIFF.
        """
        if path_geoid is not None:
            ptiff = str(path_geoid)
            for geoid in projection_list['geoid']:
                geoid_list = [path.join('.', ptiff, geoid + '.tif')]
            if not path.exists(geoid_list[0]):
                geoid_list = [geoid+'.tif' for geoid in projection_list['geoid']]
        else:
            geoid_list = [geoid+'.tif' for geoid in projection_list['geoid']]

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

    def tranform_height(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float],
                        z: Union[np.ndarray, float]) -> float:
        """
        Converting z in altitude to z in height of point.

        Args:
            x (Union[np.array, float]): x coordinate of the point.
            y (Union[np.array, float]): y coordinate of the point.
            z (Union[np.array, float]): z coordinate of the point.

        Returns:
            float: New height z.
        """
        coor_geog = self.carto_to_geog(x, y, z)
        try:
            new_z = self.geog_to_geoid(coor_geog[0],
                                       coor_geog[1],
                                       coor_geog[2])[2]
        except AttributeError:
            print("Warning: the geoid has not been entered, the z transformation from altitude "
                  "to height has not been performed, return z altitude")
            new_z = z

        if new_z == np.inf:
            raise ValueError("out geoid")
        return new_z

    def tranform_altitude(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float],
                          z: Union[np.ndarray, float]) -> float:
        """
        Converting z in height to z in altitude of point.

        Args:
            x (Union[np.array, float]): x coordinate of the point.
            y (Union[np.array, float]): y coordinate of the point.
            z (Union[np.array, float]): z coordinate of the point.

        Returns:
            float: New altitude z.
        """
        coor_geog = self.carto_to_geog(x, y, z)
        try:
            coor_geog = self.geoid_to_geog(coor_geog[0],
                                           coor_geog[1],
                                           coor_geog[2])
            new_z = self.geog_to_carto(coor_geog[0],
                                       coor_geog[1],
                                       coor_geog[2])[2]
        except AttributeError:
            print("Warning: the geoid has not been entered, the z transformation from height "
                  "to altitude has not been performed, return z height")
            new_z = z

        if np.all(new_z == np.inf):
            raise ValueError("out geoid")
        return new_z
