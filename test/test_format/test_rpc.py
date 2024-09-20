"""
Scripte to test class Rpc
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument, duplicate-code
import copy
import numpy as np
import pytest
from borea.datastruct.dtm import Dtm
from borea.datastruct.shot import Shot
from borea.datastruct.camera import Camera
from borea.format.rpc import Rpc
from borea.geodesy.proj_engine import ProjEngine
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
            np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
            "test_cam", 'degree', True, 'opk')
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
EPSG = [2154]
LIST_GEOID = ["./dataset/fr_ign_RAF20.tif"]
LIST_NO_GEOID = None
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "height"
SHOT_TYPE_Z = "altitude"


def dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def proj_singleton(epsg, geoid=None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, geoid)


def test_rpc_order1():
    shot = copy.copy(SHOT)
    cam = CAM
    proj_singleton(EPSG, LIST_GEOID)
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    param_rpc = {"size_grid": 100, "order": 1, "fact_rpc": None, "epsg_output": None}
    unit_data = {"unit_z_data": DATA_TYPE_Z, "unit_z_shot": SHOT_TYPE_Z}
    rpc = Rpc.from_shot(shot, cam, param_rpc, unit_data)
    assert rpc.fact_rpc is None
    assert rpc.param_rpc["ERR_BIAS"] == -1
    assert rpc.param_rpc["ERR_RAND"] == -1
    assert (rpc.param_rpc["SAMP_NUM_COEFF"] == np.array([0.26100828, 248.01054402, 2.49737154,
                                                         -0.26101961, 0., 0., 0., 0., 0., 0.,
                                                         0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                         0.])).all


def test_rpc_order2():
    shot = copy.copy(SHOT)
    cam = CAM
    proj_singleton(EPSG, LIST_GEOID)
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    param_rpc = {"size_grid": 100, "order": 2, "fact_rpc": 1e-6, "epsg_output": None}
    unit_data = {"unit_z_data": DATA_TYPE_Z, "unit_z_shot": SHOT_TYPE_Z}
    rpc = Rpc.from_shot(shot, cam, param_rpc, unit_data)
    assert rpc.fact_rpc == 1e-6
    assert rpc.param_rpc["ERR_BIAS"] == -1
    assert rpc.param_rpc["ERR_RAND"] == -1
    assert (rpc.param_rpc["SAMP_NUM_COEFF"] == np.array([0.26100828, 248.01054402, 2.49737154,
                                                         -0.26101961, 7.62583456e-01,
                                                         1.87520064e-02, 1.38193978e-03,
                                                         2.04518594e+01, 2.05066138e+01,
                                                         2.10524888e-05, 0., 0., 0., 0., 0.,
                                                         0., 0., 0., 0., 0.])).all


def test_rpc_order3():
    shot = copy.copy(SHOT)
    cam = CAM
    proj_singleton(EPSG, LIST_GEOID)
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    param_rpc = {"size_grid": 100, "order": 3, "fact_rpc": 1e-6, "epsg_output": None}
    unit_data = {"unit_z_data": DATA_TYPE_Z, "unit_z_shot": SHOT_TYPE_Z}
    rpc = Rpc.from_shot(shot, cam, param_rpc, unit_data)
    assert rpc.fact_rpc == 1e-6
    assert rpc.param_rpc["ERR_BIAS"] == -1
    assert rpc.param_rpc["ERR_RAND"] == -1
    assert (rpc.param_rpc["SAMP_NUM_COEFF"] == np.array([0.26100828, 248.01054402, 2.49737154,
                                                         -0.26101961, 7.62583456e-01,
                                                         1.87520064e-02, 1.38193978e-03,
                                                         2.04518594e+01, 2.05066138e+01,
                                                         2.10524888e-05, -1.46344210e-03,
                                                         -1.61998547e-01, -1.86307256e-01,
                                                         -9.23499356e-06, -3.07162634e-02,
                                                         3.03128323e-02, 1.03706630e-06,
                                                         -5.50612111e-03, -5.74032511e-03,
                                                         3.73181296e-02])).all


def test_rpc_errororder():
    shot = copy.copy(SHOT)
    cam = CAM
    proj_singleton(EPSG, LIST_GEOID)
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    param_rpc = {"size_grid": 100, "order": 4, "fact_rpc": 1e-6, "epsg_output": None}
    unit_data = {"unit_z_data": DATA_TYPE_Z, "unit_z_shot": SHOT_TYPE_Z}
    with pytest.raises(ValueError):
        Rpc.from_shot(shot, cam, param_rpc, unit_data)
