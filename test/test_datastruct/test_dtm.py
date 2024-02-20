"""
Script test for class dtm.
"""
import numpy as np
from src.datastruct.dtm import Dtm

PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"

def test_init_dtm():
    dtm = Dtm(PATH_DTM, "height")
    assert dtm.order == 1
    assert dtm.keep_in_memory == False
    assert hasattr(dtm, 'img')
    assert hasattr(dtm, 'rb')
    assert hasattr(dtm, 'gt')

def test_dtm_get_one():
    dtm = Dtm(PATH_DTM, "height")
    z = dtm.get_z_world(800000, 6280000)
    assert z == 49.533


def test_dtm_get_multi():
    dtm = Dtm(PATH_DTM, "height")
    z = dtm.get_z_world(np.array([800000,800000,800000]), np.array([6280000,6280000,6280000]))
    assert (z == np.array([49.533,49.533,49.533])).all
