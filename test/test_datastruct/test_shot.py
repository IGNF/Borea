"""
Script test for module shot
"""
import copy
from pathlib import Path, PureWindowsPath
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.local_euclidean_proj import LocalEuclideanProj
from src.datastruct.dtm import Dtm
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925,6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True)
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
EPSG = 2154
DICT_PROJ_WITH_G = {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}
DICT_PROJ_WITHOUT_G = {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'}
PATH_GEOID = Path(PureWindowsPath("./dataset/"))
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "height"
SHOT_TYPE_Z = "altitude"


def setup_module(module): # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def setup_test(): # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def Dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def Proj_singleton(epsg, proj_list = None, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, proj_list, path_geoid)


def test_set_param_eucli():
    shot = copy.copy(SHOT)
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    projeucli = LocalEuclideanProj(814975.925, 6283986.148)
    shot.set_param_eucli_shot(approx=False)
    pos_expected = projeucli.mat_to_mat_eucli(814975.925, 6283986.148, shot.mat_rot)
    assert np.all(shot.mat_rot_eucli == pos_expected)


def test_set_param_eucli_withoutgeoid():
    shot = copy.copy(SHOT)
    Proj_singleton(EPSG, DICT_PROJ_WITHOUT_G)
    projeucli = LocalEuclideanProj(814975.925, 6283986.148)
    shot.set_param_eucli_shot(approx=False)
    pos_expected = projeucli.mat_to_mat_eucli(814975.925, 6283986.148, shot.mat_rot)
    assert np.all(shot.mat_rot_eucli == pos_expected)


def test_from_shot_eucli():
    shot = copy.copy(SHOT)
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    shot.set_param_eucli_shot(approx=False)
    projeucli = LocalEuclideanProj(814975.925, 6283986.148)
    pos_shot_eucli = projeucli.world_to_eucli(np.array([814975.925, 6283986.148, 1771.280]))
    mat_rot_eucli = projeucli.mat_to_mat_eucli(814975.925, 6283986.148, shot.mat_rot)
    shot_eucli = Shot.from_param_euclidean("test_shot", pos_shot_eucli, mat_rot_eucli, "test_cam", "degree",True, False)
    assert shot.name_shot == shot_eucli.name_shot
    assert shot.pos_shot[0] == round(shot_eucli.pos_shot[0],3)
    assert shot.pos_shot[1] == round(shot_eucli.pos_shot[1],3)
    assert shot.pos_shot[2] == round(shot_eucli.pos_shot[2],3)
    assert round(shot.ori_shot[0],3) == round(shot_eucli.ori_shot[0],3)
    assert round(shot.ori_shot[1],3) == round(shot_eucli.ori_shot[1],3)
    assert round(shot.ori_shot[2],3) == round(shot_eucli.ori_shot[2],3)


def test_set_unit_angle_degree():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([np.pi,0,2*np.pi]), "test_cam", 'radian',True)
    shot.set_unit_angle("degree")
    assert shot.unit_angle == "degree"
    assert shot.ori_shot[0] == 180
    assert shot.ori_shot[1] == 0
    assert shot.ori_shot[2] == 360


def test_set_unit_angle_radian():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([180,0,360]), "test_cam", 'degree',True)
    shot.set_unit_angle("radian")
    assert shot.unit_angle == "radian"
    assert shot.ori_shot[0] == np.pi
    assert shot.ori_shot[1] == 0
    assert shot.ori_shot[2] == 2*np.pi


def test_set_unit_angle_same():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([180,0,360]), "test_cam", 'degree',True)
    shot.set_unit_angle("degree")
    assert shot.unit_angle == "degree"
    assert shot.ori_shot[0] == 180
    assert shot.ori_shot[1] == 0
    assert shot.ori_shot[2] == 360


def test_set_type_z():
    shot = copy.copy(SHOT)
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    shot.set_param_eucli_shot(approx=False)
    shot.set_type_z("height")


def test_set_linear_alteration_False():
    shot = copy.copy(SHOT)
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    shot.set_param_eucli_shot(approx=False)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    cam = CAM
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    shot.set_linear_alteration(linear_alteration=False)
    assert shot.linear_alteration == False


def test_set_linear_alteration_True():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    shot.set_param_eucli_shot(approx=False)
    cam = CAM
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    shot.set_linear_alteration(linear_alteration=True)
    assert shot.linear_alteration == True
    assert shot.pos_shot[2] == 1771.280

def test_set_z_nadir():
    shot = copy.copy(SHOT)
    shot.set_z_nadir(z_nadir=10.00)
    assert shot.z_nadir == 10.00


def test_approx_eucli_system():
    setup_test()
    shot = copy.copy(SHOT)
    shot.set_param_eucli_shot(approx=True)
    assert shot.approxeucli == True
    assert shot.projeucli.earth_raduis == 6366000
    assert (shot.projeucli.pt_central == np.array([814975.925,6283986.148,0])).all()