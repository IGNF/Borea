"""
Script test for module proj_engine
"""
from src.geodesy.proj_engine import ProjEngine


def test_get_meridian_convergence():
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    assert meridian_convergence == -1.0393503607302814
