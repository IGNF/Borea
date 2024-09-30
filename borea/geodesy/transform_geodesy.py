"""
Module for class ProjEngine, transform geodesy
"""
import pyproj
import numpy as np
import pandas as pd


# pylint: disable=too-many-instance-attributes
class TransformGeodesy():
    """
    This class provides functions to tranform coordinate system.
    Class parent of ProjEngine.
    Implemented by ProjEngine.

    Args:
        geoid (list): List of geoid to use.
        epsg (list): Code epsg of the projection ex: [2154].
        epsg_output (int): Code epsg of the output projection. If you want to change.
    """
    def __init__(self, epsg: list, geoid: list, epsg_output: int) -> None:
        self.epsg = epsg
        self.epsg_output = epsg_output
        self.crs = pyproj.CRS.from_epsg(epsg[0])
        self.geoid = geoid
        self._carto_to_geoc = None
        self._geoc_to_carto = None
        self._carto_to_geog = None
        self._geog_to_carto = None
        self._geog_to_geoid = None
        self._geoid_to_geog = None
        self._proj_to_proj_out = None

    @property
    def carto_to_geog(self) -> pyproj.Transformer:
        """
        Returns the transformation or instantiates it before returning it.

        Returns:
            pyproj.Transformer : carto_to_geog
        """
        if not self._carto_to_geog:
            try:
                crs_geog = pyproj.CRS.from_epsg(self.epsg[1])
            except (IndexError, pyproj.exceptions.CRSError):
                crs_geog = pyproj.crs.GeographicCRS(name=self.crs.name, datum=self.crs.datum.name)

            self._carto_to_geog = pyproj.Transformer.from_crs(self.crs, crs_geog).transform

        return self._carto_to_geog

    @property
    def geog_to_carto(self) -> pyproj.Transformer:
        """
        Returns the transformation or instantiates it before returning it.

        Returns:
            pyproj.Transformer : geog_to_carto
        """
        if not self._geog_to_carto:
            try:
                crs_geog = pyproj.CRS.from_epsg(self.epsg[1])
            except (IndexError, pyproj.exceptions.CRSError):
                crs_geog = pyproj.crs.GeographicCRS(name=self.crs.name, datum=self.crs.datum.name)

            self._geog_to_carto = pyproj.Transformer.from_crs(crs_geog, self.crs).transform

        return self._geog_to_carto

    @property
    def carto_to_geoc(self) -> pyproj.Transformer:
        """
        Returns the transformation or instantiates it before returning it.

        Returns:
            pyproj.Transformer : carto_to_geoc
        """
        if not self._carto_to_geoc:
            try:
                crs_geoc = pyproj.CRS.from_epsg(self.epsg[2])
            except (IndexError, pyproj.exceptions.CRSError):
                crs_geoc = pyproj.crs.GeocentricCRS(name=self.crs.name, datum=self.crs.datum.name)

            self._carto_to_geoc = pyproj.Transformer.from_crs(self.crs, crs_geoc).transform

        return self._carto_to_geoc

    @property
    def geoc_to_carto(self) -> pyproj.Transformer:
        """
        Returns the transformation or instantiates it before returning it.

        Returns:
            pyproj.Transformer : geoc_to_carto
        """
        if not self._geoc_to_carto:
            try:
                crs_geoc = pyproj.CRS.from_epsg(self.epsg[2])
            except (IndexError, pyproj.exceptions.CRSError):
                crs_geoc = pyproj.crs.GeocentricCRS(name=self.crs.name, datum=self.crs.datum.name)

            self._geoc_to_carto = pyproj.Transformer.from_crs(crs_geoc, self.crs).transform

        return self._geoc_to_carto

    @property
    def geoid_to_geog(self) -> pyproj.Transformer:
        """
        Returns the transformation or instantiates it before returning it.

        Returns:
            pyproj.Transformer : geoid_to_geog
        """
        if not self.geoid:
            raise ValueError("Mistake Geoid path")

        if not self._geoid_to_geog:
            try:
                # Transform geoide coordinates to geographic coordinates
                self._geoid_to_geog = pyproj.Transformer.from_pipeline("+proj=vgridshift "
                                                                       "+grids="
                                                                       f"{','.join(self.geoid)} "
                                                                       "+multiplier=1").transform
            except pyproj.exceptions.ProjError as e:
                raise pyproj.exceptions.ProjError(f"{self.geoid} The name or path "
                                                  "of geotif is incorrect or does not exist in "
                                                  f"{pyproj.datadir.get_data_dir()}!!!{e}") from e

        return self._geoid_to_geog

    @property
    def geog_to_geoid(self) -> pyproj.Transformer:
        """
        Returns the transformation or instantiates it before returning it.

        Returns:
            pyproj.Transformer : geog_to_geoid
        """
        if not self.geoid:
            raise ValueError("Mistake Geoid path")

        if not self._geog_to_geoid:
            try:
                # Transform geoide coordinates to geographic coordinates
                self._geog_to_geoid = pyproj.Transformer.from_pipeline("+proj=vgridshift "
                                                                       "+grids="
                                                                       f"{','.join(self.geoid)} "
                                                                       "+multiplier=-1").transform
            except pyproj.exceptions.ProjError as e:
                raise pyproj.exceptions.ProjError(f"{self.geoid} The name or path "
                                                  "of geotif is incorrect or does not exist in "
                                                  f"{pyproj.datadir.get_data_dir()}!!!{e}") from e

        return self._geog_to_geoid

    @property
    def proj_to_proj_out(self) -> pyproj.Transformer:
        """
        Create the pyproj Transformer from crs of worksite to crs geographic ask.

        Returns:
            pyproj.Transformer : carto_to_geog_out
        """
        if not self._proj_to_proj_out:
            crs_out = pyproj.CRS.from_epsg(self.epsg_output)
            self._proj_to_proj_out = pyproj.Transformer.from_crs(self.crs, crs_out).transform

        return self._proj_to_proj_out

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

        if np.all(new_z == np.inf):
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

    def transform_pt_proj(self, df_pt: pd.DataFrame, type_z_input: str = None,
                          type_z_output: str = None) -> pd.DataFrame:
        """
        Tranform the input projection to the output projection of points coordinates 
        """
        if type_z_input and type_z_output:
            if type_z_input != type_z_output:
                if type_z_output == "altitude":
                    df_pt["z"] = self.tranform_altitude(np.array([df_pt['x'],
                                                                  df_pt['y'],
                                                                  df_pt['z']]))
                if type_z_output == "height":
                    df_pt["z"] = self.tranform_height(np.array([df_pt['x'],
                                                                df_pt['y'],
                                                                df_pt['z']]))

        df_pt["x"], df_pt["y"] = self.proj_to_proj_out(df_pt['x'], df_pt['y'])

        return df_pt
