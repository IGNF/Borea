"""
Script test for module proj_engine
"""
import pyproj
import pytest
from src.datastruct.dtm import Dtm
from src.geodesy.proj_engine import ProjEngine

PATH_GEOID = ["./../dataset/fr_ign_RAF20.tif"]

def setup_module(module): # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_ProjEngine_withpathgeotiff():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, PATH_GEOID)
    proj = ProjEngine()
    assert proj.geog_to_geoid


def test_ProjEngine_notgeoid():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154)
    proj = ProjEngine()
    assert not proj.geog_to_geoid


def test_ProjEngine_notgeoidwithpathgeotiff():
    ProjEngine.clear()
    with pytest.raises(pyproj.exceptions.ProjError) as e_info:
        ProjEngine().set_epsg(2154, ["fr_ign_RAF2.tif"])


def test_get_meridian_convergence():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, PATH_GEOID)
    proj = ProjEngine()
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    theorical_value = -1.039350
    assert abs(meridian_convergence - theorical_value)<0.000001
