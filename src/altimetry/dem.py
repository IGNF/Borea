"""
A module for manipulating a digital elevation model.
"""
from pathlib import Path
from typing import Union, Any, Tuple
import numpy as np
from osgeo import gdal
from scipy import ndimage
from src.utils.conversion import change_dim
gdal.UseExceptions()


# pylint: disable-next=too-many-instance-attributes
class Dem:
    """
    Represents a digital elevation model.

    Args:
        path_dem (str): path to the dem file. If None Dem.get() always returns  0.
        order (int): The method of interpolation to perform.
                    0 : nearest, 1 : slinear, 3 : cubic, 5 : quintic.
        cval (int): Value to fill past edges of dem.
                    If None raise an error for any point outside the dem.
        keep_in_memory (bool): Store all data in memory.

    .. note::
        All gdal formats are supported. The file must contain georeferencing information.
    """
    # pylint: disable-next=too-many-arguments
    def __init__(self, path_dem: str, type_dem: str, order: int = 1, cval: Union[int, None] = None,
                 keep_in_memory: bool = False):
        """
        Initiate a Dem object from a file path.

        Args:
            path_dem (str): path to the dem file.
            type (str): Type of dem "a" altitude, "h" height.
            order (int): The method of interpolation to perform.
                        0:nearest 1:bilinear 3:cubic 5:quintic.
            cval (int): Value to fill past edges of dem or nodata.
                        If None raise an error for any point outside the dem or Nodata.
            keep_in_memory (bool): Store all image in memory.
        """
        gdal.AllRegister()
        self.type_dem = type_dem
        self.order = order
        self.keep_in_memory = keep_in_memory
        self.path_dem = Path(path_dem)
        self.img = gdal.Open(self.path_dem.as_posix())
        self.rb = self.img.GetRasterBand(1)
        self.gt = self.img.GetGeoTransform()
        self.cval = cval if cval is not None else np.nan
        self.nodata = self.rb.GetNoDataValue()
        if self.keep_in_memory:
            self.array = self.rb.ReadAsArray()

    def image_to_world(self, c: Union[int, float, list, np.ndarray],
                       l: Union[int, float, list, np.ndarray]) -> Tuple[Any, Any]:
        """
        Compute world coordinates from image coordinates.

        Args:
            c (Union[int, float, list, np.ndarray]): Column coordinates.
            l (Union[int, float, list, np.ndarray]): Line coordinates.

        Returns:
            Tuple[Any, Any]: x, y world coordinates.
        """
        if self.gt:
            x = (np.array(c)+0.5) * self.gt[1] + self.gt[0]
            y = (np.array(l)+0.5) * self.gt[5] + self.gt[3]
        else:
            x, y = np.nan, np.nan
        return x, y

    def world_to_image(self, x: Union[int, float, list, np.ndarray],
                       y: Union[int, float, list, np.ndarray]) -> Tuple[Any, Any]:
        """
        Compute image coordinates from world coordinates.

        Args:
            x (Union[int, float, list, np.ndarray]): x world coordinate.
            y (Union[int, float, list, np.ndarray]): y world coordinate.

        Returns:
            Tuple[Any, Any]: Image coordinates.
        """
        if self.gt:
            col = (np.array(x) - self.gt[0])/self.gt[1] - 0.5
            line = (np.array(y) - self.gt[3])/self.gt[5] - 0.5
        else:
            col, line = np.nan, np.nan
        return col, line

    def get(self, x: Union[int, float, np.ndarray],
            y: Union[int, float, np.ndarray]) -> Any:
        """
        Extract value in the Dem.

        Args:
            x (Union[int, float, np.ndarray]): x world coordinate.
            y (Union[int, float, np.ndarray]): y world coordinate.

        Returns:
            Union[int, float, list, np.ndarray]: z value.
        """
        if isinstance(x, np.ndarray):
            dim = np.shape(x)
        else:
            dim = ()

        x, y, = np.array(x), np.array(y)
        if self.path_dem is None:
            return np.zeros_like(x)
        col, line = self.world_to_image(x, y)
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
            z = ndimage.map_coordinates(self.array, np.vstack([line, col]),
                                        order=self.order, mode="constant", cval=self.cval)
        if np.any(np.isnan(z)):
            raise IndexError(f"Out dem {x} {y}")

        if dim == ():
            z = z[0]
        z = change_dim(np.array(z, dtype=float), dim)
        return np.round(z, 3)
