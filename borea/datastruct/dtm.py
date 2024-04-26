"""
A module for manipulating a digital elevation model.
"""
from pathlib import Path, PureWindowsPath
import numpy as np
from osgeo import gdal
from scipy import ndimage
from borea.transform_world_image.transform_dtm.world_image_dtm import WorldImageDtm
from borea.utils.singleton.singleton import Singleton
gdal.UseExceptions()


# pylint: disable-next=too-many-instance-attributes
class Dtm(WorldImageDtm, metaclass=Singleton):
    """
    Represents a digital elevation model.

    Args:
        path_dtm (str): Path to the dtm file. If None Dtm.get() always returns  0.
        order (int): The method of interpolation to perform.
                    0 : nearest, 1 : slinear, 3 : cubic, 5 : quintic.
        cval (int): Value to fill past edges of dtm.
                    If None raise an error for any point outside the dtm.
        keep_in_memory (bool): Store all data in memory.

    .. note::
        All gdal formats are supported. The file must contain georeferencing information.
    """
    def __init__(self):
        self.path_dtm = None
        self.type_dtm = None
        self.order = 1
        self.keep_in_memory = False
        self.cval = np.nan
        self.img = None
        self.rb = None
        self.nodata = None
        self.dtm_array = None
        WorldImageDtm.__init__(self, None)

    def set_dtm(self, path_dtm: str, type_dtm: str) -> None:
        """
        Set the dtm path for reading dtm.

        Args:
            path_dtm (str): Path to the dtm file.
            type (str): Type of dtm "a" altitude, "h" height.
        """
        if path_dtm:
            gdal.AllRegister()
            self.type_dtm = type_dtm
            self.path_dtm = Path(PureWindowsPath(path_dtm))
            self.img = gdal.Open(self.path_dtm.as_posix())
            self.rb = self.img.GetRasterBand(1)
            self.nodata = self.rb.GetNoDataValue()
            if self.keep_in_memory:
                self.dtm_array = self.rb.ReadAsArray()
            WorldImageDtm.__init__(self, self.img.GetGeoTransform())
        else:
            self.path_dtm = path_dtm

    def set_order(self, order: int) -> None:
        """
        The method of interpolation to perform.
        0:nearest 1:bilinear 3:cubic 5:quintic.

        Args:
            order (int): The method of interpolation to perform.
        """
        self.order = order

    def set_cval(self, cval: int) -> None:
        """
        Value to fill past edges of dtm or nodata.
        If None raise an error for any point outside the dtm or Nodata.

        Args
            cval (int): Value to fill past edges of dtm or nodata.
        """
        self.cval = cval if cval else np.nan

    def set_keep_memory(self, keep_memory: bool) -> None:
        """
        Store all image in memory.

        Args:
            keep_in_memory (bool): Store all image in memory.
        """
        self.keep_in_memory = keep_memory

    def get_z_world(self, coor_2d: np.ndarray) -> np.ndarray:
        """
        Extract value in the Dtm.

        Args:
            coor_2d (np.array): World coordinate 2D [X, Y].

        Returns:
            np.array: z value.
        """
        if self.path_dtm is None:
            return np.zeros_like(coor_2d[0])
        col, line = self.world_to_image(coor_2d)
        if not self.keep_in_memory:
            z = []
            if isinstance(col, float):
                col, line = [col], [line]
            for colt, linet in zip(col, line):
                try:
                    z += [self.rb.ReadAsArray(colt, linet, 1, 1, resample_alg=self.order)]
                except RuntimeError:
                    z += [self.cval]
        else:
            z = ndimage.map_coordinates(self.dtm_array, np.vstack([line, col]),
                                        order=self.order, mode="constant", cval=self.cval)
        if np.any(np.isnan(z)):
            raise IndexError(f"Out dtm {coor_2d[0]} {coor_2d[1]}")

        return np.round(np.array(z, dtype=float), 3)
