"""
Script test for module shot
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument, duplicate-code
import copy
import numpy as np
from borea.datastruct.shot import Shot
from borea.datastruct.camera import Camera
from borea.geodesy.proj_engine import ProjEngine
from borea.geodesy.local_euclidean_proj import LocalEuclideanProj
from borea.datastruct.dtm import Dtm
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
            np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
            "test_cam", 'degree', True, "opk")
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
EPSG = [2154]
LIST_GEOID = ["./dataset/fr_ign_RAF20.tif"]
LIST_NO_GEOID = None
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "height"
SHOT_TYPE_Z = "altitude"


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def setup_test():  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def proj_singleton(epsg, path_geoid=None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, path_geoid)


def test_set_param_eucli():
    shot = copy.copy(SHOT)
    proj_singleton(EPSG, LIST_GEOID)
    projeucli = LocalEuclideanProj(814975.925, 6283986.148)
    shot.set_param_eucli_shot(approx=False)
    pos_expected = projeucli.mat_to_mat_eucli(814975.925, 6283986.148, shot.mat_rot)
    assert np.all(shot.mat_rot_eucli == pos_expected)


def test_set_param_eucli_withoutgeoid():
    shot = copy.copy(SHOT)
    proj_singleton(EPSG, LIST_NO_GEOID)
    projeucli = LocalEuclideanProj(814975.925, 6283986.148)
    shot.set_param_eucli_shot(approx=False)
    pos_expected = projeucli.mat_to_mat_eucli(814975.925, 6283986.148, shot.mat_rot)
    assert np.all(shot.mat_rot_eucli == pos_expected)


def test_from_shot_eucli():
    shot = copy.copy(SHOT)
    proj_singleton(EPSG, LIST_GEOID)
    shot.set_param_eucli_shot(approx=False)
    projeucli = LocalEuclideanProj(814975.925, 6283986.148)
    pos_shot_eucli = projeucli.world_to_eucli(np.array([814975.925, 6283986.148, 1771.280]))
    mat_rot_eucli = projeucli.mat_to_mat_eucli(814975.925, 6283986.148, shot.mat_rot)
    shot_eucli = Shot.from_param_euclidean("test_shot", pos_shot_eucli, mat_rot_eucli,
                                           "test_cam", "degree", True, "opk", False)
    assert shot.name_shot == shot_eucli.name_shot
    assert shot.pos_shot[0] == round(shot_eucli.pos_shot[0], 3)
    assert shot.pos_shot[1] == round(shot_eucli.pos_shot[1], 3)
    assert shot.pos_shot[2] == round(shot_eucli.pos_shot[2], 3)
    assert round(shot.ori_shot[0], 3) == round(shot_eucli.ori_shot[0], 3)
    assert round(shot.ori_shot[1], 3) == round(shot_eucli.ori_shot[1], 3)
    assert round(shot.ori_shot[2], 3) == round(shot_eucli.ori_shot[2], 3)


def test_set_unit_angle_degree():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
                np.array([np.pi, 0, 2*np.pi]), "test_cam", 'radian', True, "opk")
    shot.set_unit_angle("degree")
    assert shot.unit_angle == "degree"
    assert shot.ori_shot[0] == 180
    assert shot.ori_shot[1] == 0
    assert shot.ori_shot[2] == 360


def test_set_unit_angle_radian():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
                np.array([180, 0, 360]), "test_cam", 'degree', True, "opk")
    shot.set_unit_angle("radian")
    assert shot.unit_angle == "radian"
    assert shot.ori_shot[0] == np.pi
    assert shot.ori_shot[1] == 0
    assert shot.ori_shot[2] == 2*np.pi


def test_set_unit_angle_same():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
                np.array([180, 0, 360]), "test_cam", 'degree', True, "opk")
    shot.set_unit_angle("degree")
    assert shot.unit_angle == "degree"
    assert shot.ori_shot[0] == 180
    assert shot.ori_shot[1] == 0
    assert shot.ori_shot[2] == 360


def test_set_type_z():
    shot = copy.copy(SHOT)
    proj_singleton(EPSG, LIST_GEOID)
    shot.set_param_eucli_shot(approx=False)
    shot.set_type_z("height")


def test_set_linear_alteration_false():
    shot = copy.copy(SHOT)
    proj_singleton(EPSG, LIST_GEOID)
    shot.set_param_eucli_shot(approx=False)
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    cam = CAM
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    shot.set_linear_alteration(linear_alteration=False)
    assert shot.linear_alteration is False


def test_set_linear_alteration_true():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
                np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                "test_cam", 'degree', True, "opk")
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    proj_singleton(EPSG, LIST_GEOID)
    shot.set_param_eucli_shot(approx=False)
    cam = CAM
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    shot.set_linear_alteration(linear_alteration=True)
    assert shot.linear_alteration is True
    assert shot.pos_shot[2] == 1771.280


def test_set_z_nadir():
    shot = copy.copy(SHOT)
    shot.set_z_nadir(z_nadir=10.00)
    assert shot.z_nadir == 10.00


def test_approx_eucli_system():
    setup_test()
    shot = copy.copy(SHOT)
    shot.set_param_eucli_shot(approx=True)
    assert shot.approxeucli is True
    assert shot.projeucli.earth_raduis == 6366000
    assert (shot.projeucli.pt_central == np.array([814975.925, 6283986.148, 0])).all()


def test_set_order_axe():
    setup_test()
    shot = copy.copy(SHOT)
    shot.set_order_axe("pok")
    assert (shot.ori_shot != [-0.245070686036, -0.069409621323, 0.836320989726]).all()


def test_set_proj():
    setup_test()
    shot = Shot("test_shot", np.array([657945.43, 6860369.44, 1771.280]),
                np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                "test_cam", 'degree', True, "opk")
    ProjEngine().set_epsg(EPSG, LIST_GEOID, 4326)
    shot.set_proj_pos()
    assert (np.round(shot.pos_shot, 3) == [48.842, 2.427, 1771.280]).all()
