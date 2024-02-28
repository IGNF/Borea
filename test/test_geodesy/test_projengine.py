"""
Script test for module proj_engine
"""
from src.geodesy.proj_engine import ProjEngine


def test_ProjEngine_withpathgeotiff():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    proj = ProjEngine()
    assert proj.geog_to_geoid


def test_ProjEngine_notgeoid():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    proj = ProjEngine()
    assert not proj.geog_to_geoid


def test_ProjEngine_notgeoidwithpathgeotiff():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'}, "./dataset/")
    proj = ProjEngine()
    assert not proj.geog_to_geoid


def test_get_meridian_convergence():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    proj = ProjEngine()
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    assert meridian_convergence == -1.0393503607302814
