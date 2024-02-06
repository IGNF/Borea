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
    z = dem.get(792863, 6336461)
    assert z == 199.791


def test_dem_get_multi():
    dem = Dem(PATH_DEM, "height")
    z = dem.get(np.array([792863,792863,792863]), np.array([6336461,6336461,6336461]))
    assert (z == np.array([199.791,199.791,199.791])).all
