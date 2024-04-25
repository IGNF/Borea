"""
Script to test module approx euclidean system
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
import numpy as np
import pytest
from src.datastruct.dtm import Dtm
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.approx_euclidean_proj import ApproxEuclideanProj


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_approxeuclideanproj():
    app = ApproxEuclideanProj(0, 0)
    m1 = app.mat_eucli_to_mat(0, 0, np.eye(3))
    m2 = app.mat_to_mat_eucli(0, 0, np.zeros((3, 3)))
    assert app.earth_raduis == 6366000
    assert (m1 == np.eye(3)).all()
    assert (m2 == np.zeros((3, 3))).all()


def test_world_to_eucli():
    app = ApproxEuclideanProj(554879.204, 6924210.113)
    xe, ye, ze = app.world_to_eucli(np.array([554479.204, 6924910.113, 1000]))
    assert xe == pytest.approx(-400.063, 0.001)
    assert ye == pytest.approx(700.101, 0.001)
    assert ze == pytest.approx(999.949, 0.001)


def test_eucli_to_world():
    app = ApproxEuclideanProj(554879.204, 6924210.113)
    x, y, z = app.eucli_to_world(np.array([-400.063, 700.101, 999.949]))
    assert x == pytest.approx(554479.204, 0.001)
    assert y == pytest.approx(6924910.113, 0.001)
    assert z == pytest.approx(1000, 0.001)
