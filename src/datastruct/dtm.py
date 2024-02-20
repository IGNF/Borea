"""
A module for manipulating a digital elevation model.
"""
from pathlib import Path, PureWindowsPath
from typing import Union, Any
import numpy as np
from osgeo import gdal
from scipy import ndimage
from src.utils.conversion import change_dim
from src.transform_world_image.transform_dtm.world_image_dtm import WorldImageDtm
gdal.UseExceptions()


# pylint: disable-next=too-many-instance-attributes
class Dtm(WorldImageDtm):
    """
    Represents a digital elevation model.

    Args:
        path_dtm (str): path to the dtm file. If None Dtm.get() always returns  0.
        order (int): The method of interpolation to perform.
                    0 : nearest, 1 : slinear, 3 : cubic, 5 : quintic.
        cval (int): Value to fill past edges of dtm.
                    If None raise an error for any point outside the dtm.
        keep_in_memory (bool): Store all data in memory.

    .. note::
        All gdal formats are supported. The file must contain georeferencing information.
    """
    # pylint: disable-next=too-many-arguments
    def __init__(self, path_dtm: str, type_dtm: str, order: int = 1, cval: Union[int, None] = None,
                 keep_in_memory: bool = False):
        """
        Initiate a Dtm object from a file path.

        Args:
            path_dtm (str): path to the dtm file.
            type (str): Type of dtm "a" altitude, "h" height.
            order (int): The method of interpolation to perform.
                        0:nearest 1:bilinear 3:cubic 5:quintic.
            cval (int): Value to fill past edges of dtm or nodata.
                        If None raise an error for any point outside the dtm or Nodata.
            keep_in_memory (bool): Store all image in memory.
        """
        gdal.AllRegister()
        self.type_dtm = type_dtm
        self.order = order
        self.keep_in_memory = keep_in_memory
        self.path_dtm = Path(PureWindowsPath(path_dtm))
        self.img = gdal.Open(self.path_dtm.as_posix())
        self.rb = self.img.GetRasterBand(1)
        self.cval = cval if cval is not None else np.nan
        self.nodata = self.rb.GetNoDataValue()
        if self.keep_in_memory:
            self.array = self.rb.ReadAsArray()
        super().__init__(self.img.GetGeoTransform())

    def get_z_world(self, x: Union[int, float, np.ndarray],
                    y: Union[int, float, np.ndarray]) -> Any:
        """
        Extract value in the Dtm.

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
        if self.path_dtm is None:
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
            raise IndexError(f"Out dtm {x} {y}")

        if dim == ():
            z = z[0]
        z = change_dim(np.array(z, dtype=float), dim)
        return np.round(z, 3)
