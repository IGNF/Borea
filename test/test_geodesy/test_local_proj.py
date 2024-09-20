"""
Script test for module euclidean_proj
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
import numpy as np
from borea.geodesy.proj_engine import ProjEngine
from borea.geodesy.local_euclidean_proj import LocalEuclideanProj
from borea.datastruct.dtm import Dtm


EPSG = [2154]
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def proj_singleton(epsg, path_geoid=None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, path_geoid)


def test_world_to_eucli_withfloat():
    proj_singleton(EPSG, PATH_GEOID)
    euproj = LocalEuclideanProj(0, 0)
    x, y, z = euproj.world_to_eucli(np.array([0, 0, 0]))
    print(x, y, z)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_world_to_eucli_witharray3():
    pt = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
    proj_singleton(EPSG, PATH_GEOID)
    euproj = LocalEuclideanProj(0, 0)
    x, y, z = euproj.world_to_eucli(pt)
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_world_to_eucli_witharray1():
    pt = np.array([[0], [0], [0]])
    proj_singleton(EPSG, PATH_GEOID)
    euproj = LocalEuclideanProj(0, 0)
    x, y, z = euproj.world_to_eucli(pt)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_eucli_to_world_withfloat():
    pt = np.array([0.0, 0.0, 0.0])
    proj_singleton(EPSG, PATH_GEOID)
    euproj = LocalEuclideanProj(0.0, 0.0)
    x, y, z = euproj.eucli_to_world(pt)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_eucli_to_world_witharray3():
    pt = np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
    proj_singleton(EPSG, PATH_GEOID)
    euproj = LocalEuclideanProj(0.0, 0.0)
    x, y, z = euproj.eucli_to_world(pt)
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_eucli_to_world_witharray1():
    pt = np.array([[0], [0], [0]])
    proj_singleton(EPSG, PATH_GEOID)
    euproj = LocalEuclideanProj(0.0, 0.0)
    x, y, z = euproj.eucli_to_world(pt)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0
