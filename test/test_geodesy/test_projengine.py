"""
Script test for module proj_engine
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument, duplicate-code
import pyproj
import pytest
from borea.datastruct.dtm import Dtm
from borea.geodesy.proj_engine import ProjEngine


EPSG = [2154]
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_projengine_notgeoid():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG)
    with pytest.raises(ValueError):
        _ = ProjEngine().tf.geog_to_geoid


def test_projengine_notgeoidwithpathgeotiff():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, ["fr_ign_RAF2.tif"])
    with pytest.raises(pyproj.exceptions.ProjError):
        _ = ProjEngine().tf.geog_to_geoid


def test_get_meridian_convergence():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, PATH_GEOID)
    proj = ProjEngine()
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    theorical_value = -1.039350
    assert abs(meridian_convergence - theorical_value) < 0.000001


def test_tf_create_tf_output():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, PATH_GEOID, 4326)
    proj = ProjEngine()
    assert proj.tf.proj_to_proj_out


def test_tf_conv_tf_output():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, PATH_GEOID, 4326)
    proj = ProjEngine()
    xf = 657945.43
    yf = 6860369.44
    ym = 2.427
    xm = 48.842
    xmo, ymo = proj.tf.proj_to_proj_out(xf, yf)
    assert round(xmo, 3) == xm
    assert round(ymo, 3) == ym
