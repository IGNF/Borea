"""
Script test for module ImageWorldShot
"""
import copy
from pathlib import Path, PureWindowsPath
import pytest
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True)
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
EPSG = 2154
DICT_PROJ_WITH_G = {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}
DICT_PROJ_WITHOUT_G = {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'}
PATH_GEOID = Path(PureWindowsPath("./dataset/"))
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "height"
SHOT_TYPE_Z = "altitude"


def Dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def Proj_singleton(epsg, proj_list = None, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, proj_list, path_geoid)


def test_image_to_world():
    point_image = np.array([24042.25, 14781.17])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    actual = ImageWorldShot(shot, cam).image_to_world(point_image, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0] - 815601.510),abs(actual[1] - 6283629.280),abs(actual[2] - 54.960))
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 3


def test_image_to_world_sametype_withoutgeoid():
    point_image = np.array([24042.25, 14781.17])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITHOUT_G)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    actual = ImageWorldShot(shot,cam).image_to_world(point_image, DATA_TYPE_Z, DATA_TYPE_Z)


def test_image_to_world_withoutdtm():
    point_image = np.array([24042.25, 14781.17])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(None, None)
    shot.set_param_eucli_shot(approx=False)
    with pytest.raises(ValueError) as e_info:
        z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'height', 'height', False)[2]
        shot.set_z_nadir(z_nadir)
        actual = ImageWorldShot(shot,cam).image_to_world(point_image, DATA_TYPE_Z, SHOT_TYPE_Z)


def test_image_to_world_multipoint():
    c = np.array([24042.25, 24042.25])
    l = np.array([14781.17, 14781.17])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'height', 'height', False)[2]
    shot.set_z_nadir(z_nadir)
    actual = ImageWorldShot(shot,cam).image_to_world(np.array([c, l]), DATA_TYPE_Z, SHOT_TYPE_Z)
    assert abs(actual[0,0] - 815601.510) < 1
    assert abs(actual[1,0] - 6283629.280) < 1
    assert abs(actual[2,0] - 54.960) < 3


def test_image_to_world_approx():
    Dtm.clear()
    ProjEngine.clear()
    point_image = np.array([24042.25, 14781.17])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=True)
    actual = ImageWorldShot(shot, cam).image_to_world(point_image, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0] - 815601.510),abs(actual[1] - 6283629.280),abs(actual[2] - 54.960))
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 3