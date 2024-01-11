"""
Script test for module euclidean_proj
"""
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


def test_world_to_euclidean():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    euproj = EuclideanProj(0,0,proj)
    x,y,z = euproj.world_to_euclidean(0,0,0)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0


def test_euclidean_to_world():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    euproj = EuclideanProj(0.0,0.0,proj)
    x,y,z = euproj.euclidean_to_world(0.0,0.0,0.0)
    assert round(x) == 0
    assert round(y) == 0
    assert round(z) == 0