"""
Script test for module euclidean_proj
"""
import numpy as np
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


def Proj_singleton(epsg, proj_list = None, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, proj_list, path_geoid)


def test_world_to_euclidean_withfloat():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = EuclideanProj(0,0)
    x,y,z = euproj.world_to_euclidean(0,0,0)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_world_to_euclidean_witharray3():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = EuclideanProj(0,0)
    x,y,z = euproj.world_to_euclidean(np.array([0,1,2]),np.array([0,1,2]),np.array([0,1,2]))
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_world_to_euclidean_witharray1():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = EuclideanProj(0,0)
    x,y,z = euproj.world_to_euclidean(np.array([0]),np.array([0]),np.array([0]))
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_euclidean_to_world1_withfloat():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = EuclideanProj(0.0,0.0)
    x,y,z = euproj.euclidean_to_world(0.0,0.0,0.0)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_euclidean_to_world_witharray3():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = EuclideanProj(0.0,0.0)
    x,y,z = euproj.euclidean_to_world(np.array([0,1,2]),np.array([0,1,2]),np.array([0,1,2]))
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0


def test_euclidean_to_world_witharray1():
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    euproj = EuclideanProj(0.0,0.0)
    x,y,z = euproj.euclidean_to_world(np.array([0]),np.array([0]),np.array([0]))
    assert round(x[0]) == 0
    assert round(y[0]) == 0
    assert round(z[0]) == 0
