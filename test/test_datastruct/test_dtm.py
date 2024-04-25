"""
Script test for class dtm.
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
from pathlib import Path, PureWindowsPath
import numpy as np
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def dtm_singleton(path, type_dtm):
    Dtm().set_dtm(path, type_dtm)


def test_init_dtm():
    dtm_singleton(PATH_DTM, "height")
    dtm = Dtm()
    assert dtm.order == 1
    assert dtm.keep_in_memory is False
    assert hasattr(dtm, 'img')
    assert hasattr(dtm, 'rb')
    assert hasattr(dtm, 'gt')


def test_dtm_get_one():
    dtm_singleton(PATH_DTM, type_dtm="height")
    dtm = Dtm()
    z = dtm.get_z_world(np.array([800000, 6280000]))
    assert z == 49.533


def test_dtm_get_oneplusshape():
    dtm_singleton(PATH_DTM, type_dtm="height")
    dtm = Dtm()
    z = dtm.get_z_world(np.array([[800000], [6280000]]))
    assert z == 49.533


def test_dtm_get_multi():
    dtm_singleton(PATH_DTM, type_dtm="height")
    dtm = Dtm()
    z = dtm.get_z_world(np.array([[800000, 800000, 800000], [6280000, 6280000, 6280000]]))
    assert (z == np.array([49.533, 49.533, 49.533])).all


def test_dtm_singleton():
    dtm1 = Dtm(path_dtm=PATH_DTM, type_dtm="height")
    dtm2 = Dtm()
    assert dtm1 == dtm2
    assert dtm1.path_dtm == Path(PureWindowsPath(PATH_DTM))
    assert dtm2.path_dtm == Path(PureWindowsPath(PATH_DTM))


def test_dtm_singletonclear():
    dtm_singleton(path=PATH_DTM, type_dtm="height")
    dtm1 = Dtm()
    dtm_singleton(path=None, type_dtm=None)
    dtm3 = Dtm()
    assert dtm1.path_dtm is None
    assert dtm3.path_dtm is None
