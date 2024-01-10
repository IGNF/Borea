"""
Script test to geodesy file
"""
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj

def test_get_meridian_convergence():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    assert meridian_convergence == -1.0393503607302814


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
    