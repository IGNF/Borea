"""
Script test for module euclidean_proj
"""
import numpy as np
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.local_euclidean_proj import LocalEuclideanProj
from src.datastruct.dtm import Dtm

def setup_module(module): # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def Proj_singleton(epsg, proj_list = None, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, proj_list, path_geoid)


def test_world_to_eucli_withfloat():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = LocalEuclideanProj(0,0)
    x,y,z = euproj.world_to_eucli(np.array([0,0,0]))
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_world_to_eucli_witharray3():
    pt = np.array([[0,1,2],[0,1,2],[0,1,2]])
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = LocalEuclideanProj(0,0)
    x,y,z = euproj.world_to_eucli(pt)
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_world_to_eucli_witharray1():
    pt = np.array([[0],[0],[0]])
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = LocalEuclideanProj(0,0)
    x,y,z = euproj.world_to_eucli(pt)
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_eucli_to_world1_withfloat():
    pt = np.array([0.0,0.0,0.0])
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = LocalEuclideanProj(0.0,0.0)
    x,y,z = euproj.eucli_to_world(pt)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_eucli_to_world_witharray3():
    pt = np.array([[0,1,2],[0,1,2],[0,1,2]])
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = LocalEuclideanProj(0.0,0.0)
    x,y,z = euproj.eucli_to_world(pt)
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_eucli_to_world_witharray1():
    pt = np.array([[0],[0],[0]])
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = LocalEuclideanProj(0.0,0.0)
    x,y,z = euproj.eucli_to_world(pt)
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0
