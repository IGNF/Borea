"""
Module for class ProjEngine, transform geodesy
"""
from dataclasses import dataclass
import pyproj
import numpy as np


# pylint: disable=unsubscriptable-object
@dataclass
class TransformGeodesy():
    """
    This class provides functions to tranform coordinate system.
    Class parent of ProjEngine.
    Implemented by ProjEngine.

    Args:
        geoid (list): List of geoid to use.
        crs (pyproj): CRS pyproj of the worksite.
    """
    carto_to_geoc = None
    geoc_to_carto = None
    carto_to_geog = None
    geog_to_carto = None
    geog_to_geoid = None
    geoid_to_geog = None

    def __tf_init__(self, geoid: list, crs: pyproj) -> None:
        crs_geoc = pyproj.crs.GeocentricCRS(name=crs.name, datum=crs.datum.name)
        crs_geog = pyproj.crs.GeographicCRS(name=crs.name, datum=crs.datum.name)
        # Transform cartographic coordinates to geographic coordinates
        self.carto_to_geog = pyproj.Transformer.from_crs(crs, crs_geog).transform
        # Transform geographic coordinates to cartographic coordinates
        self.geog_to_carto = pyproj.Transformer.from_crs(crs_geog, crs).transform
        # Transform cartographic coordinates to geocentric coordinates
        self.carto_to_geoc = pyproj.Transformer.from_crs(crs, crs_geoc).transform
        # Transform geocentric coordinates to cartographic coordinates
        self.geoc_to_carto = pyproj.Transformer.from_crs(crs_geoc, crs).transform

        if geoid:
            self.tf_geoid(geoid)

    def tf_geoid(self, geoid: list) -> None:
        """
        Create attribute transform, to transform geographic coordinates to geoide coordinates.

        Args:
            geoid (list): List of geoid to use.
        """
        try:
            # Transform geoide coordinates to geographic coordinates
            self.geoid_to_geog = pyproj.Transformer.from_pipeline(f"+proj=vgridshift "
                                                                  f"+grids={','.join(geoid)} "
                                                                  "+multiplier=1").transform
            # Transform geographic coordinates to geoide coordinates
            self.geog_to_geoid = pyproj.Transformer.from_pipeline(f"+proj=vgridshift "
                                                                  f"+grids={','.join(geoid)} "
                                                                  "+multiplier=-1").transform
        except pyproj.exceptions.ProjError as e:
            raise pyproj.exceptions.ProjError(f"{geoid} The name or path of geotif is incorrect or "
                                              "does not exist in "
                                              f"{pyproj.datadir.get_data_dir()}!!!{e}") from e

    def tranform_height(self, coor: np.ndarray) -> float:
        """
        Converting z in altitude to z in height of point.

        Args:
            coor (np.array): [X, Y, Z] coordinate of the point.

        Returns:
            float: New height Z.
        """
        coor_geog = self.carto_to_geog(coor[0], coor[1], coor[2])
        try:
            coor_geog = self.geoid_to_geog(coor_geog[0],
                                           coor_geog[1],
                                           coor_geog[2])
            new_z = self.geog_to_carto(coor_geog[0],
                                       coor_geog[1],
                                       coor_geog[2])[2]
        except AttributeError as info:
            raise ValueError("The geoid has not been entered, "
                             "cannot transform z altitude to height.") from info

        if new_z == np.inf:
            raise ValueError("out geoid")
        return new_z

    def tranform_altitude(self, coor: np.ndarray) -> float:
        """
        Converting z in height to z in altitude of point.

        Args:
            coor (np.array): [X, Y, Z] coordinate of the point.

        Returns:
            float: New altitude Z.
        """
        coor_geog = self.carto_to_geog(coor[0], coor[1], coor[2])
        try:
            coor_geog = self.geog_to_geoid(coor_geog[0],
                                           coor_geog[1],
                                           coor_geog[2])
            new_z = self.geog_to_carto(coor_geog[0],
                                       coor_geog[1],
                                       coor_geog[2])[2]
        except AttributeError as info:
            raise ValueError("The geoid has not been entered, "
                             "cannot transform z height to altitude.") from info

        if np.all(new_z == np.inf):
            raise ValueError("out geoid")
        return new_z
