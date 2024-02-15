"""
Script test for class dem.
"""
import numpy as np
from src.altimetry.dem import Dem

PATH_DEM = "./test/data/MNT_France_25m_h_crop.tif"

def test_init_dem():
    dem = Dem(PATH_DEM, "height")
    assert dem.order == 1
    assert dem.keep_in_memory == False
    assert hasattr(dem, 'img')
    assert hasattr(dem, 'rb')
    assert hasattr(dem, 'gt')

def test_dem_get_one():
    dem = Dem(PATH_DEM, "height")
    z = dem.get(800000, 6280000)
    assert z == 49.533


def test_dem_get_multi():
    dem = Dem(PATH_DEM, "height")
    z = dem.get(np.array([800000,800000,800000]), np.array([6280000,6280000,6280000]))
    assert (z == np.array([49.533,49.533,49.533])).all
