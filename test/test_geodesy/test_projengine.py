"""
Script test for module proj_engine
"""
from src.geodesy.proj_engine import ProjEngine


def test_ProjEngine_withpathgeotiff():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./test/data/")
    assert hasattr(proj.tf, 'geog_to_geoid')


def test_ProjEngine_notgeoid():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    assert not hasattr(proj.tf, 'geog_to_geoid')


def test_ProjEngine_notgeoidwithpathgeotiff():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'}, "./test/data/")
    assert not hasattr(proj.tf, 'geog_to_geoid')


def test_get_meridian_convergence():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./test/data/")
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    assert meridian_convergence == -1.0393503607302814
