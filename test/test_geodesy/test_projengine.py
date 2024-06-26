"""
Script test for module proj_engine
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
import pyproj
import pytest
from borea.datastruct.dtm import Dtm
from borea.geodesy.proj_engine import ProjEngine


PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_projengine_withpathgeotiff():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, PATH_GEOID)
    proj = ProjEngine()
    assert proj.geog_to_geoid


def test_projengine_notgeoid():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154)
    proj = ProjEngine()
    assert not proj.geog_to_geoid


def test_projengine_notgeoidwithpathgeotiff():
    ProjEngine.clear()
    with pytest.raises(pyproj.exceptions.ProjError):
        ProjEngine().set_epsg(2154, ["fr_ign_RAF2.tif"])


def test_get_meridian_convergence():
    ProjEngine.clear()
    ProjEngine().set_epsg(2154, PATH_GEOID)
    proj = ProjEngine()
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    theorical_value = -1.039350
    assert abs(meridian_convergence - theorical_value) < 0.000001
