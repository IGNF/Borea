"""
Script test for module WorldImageShot
"""
import copy
from pathlib import Path, PureWindowsPath
import pytest
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm
from src.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True)
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
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


def test_world_to_image():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', nonadir=False)[2]
    shot.set_z_nadir(z_nadir)
    actual = WorldImageShot(shot, cam).world_to_image(point_terrain, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0] - 24042.25), abs(actual[1] - 14781.17))
    assert abs(actual[0] - 24042.25) < 1
    assert abs(actual[1] - 14781.17) < 1


def test_world_to_image_multipoints():
    point_terrain = np.array([[815601.510,815601.510,815601.510],
                              [6283629.280,6283629.280,6283629.280],
                              [54.960,54.960,54.960]])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', nonadir=False)[2]
    shot.set_z_nadir(z_nadir)
    actual = WorldImageShot(shot,cam).world_to_image(point_terrain, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0,0] - 24042.25), abs(actual[1,0] - 14781.17))
    assert abs(actual[0,0] - 24042.25) < 1
    assert abs(actual[1,0] - 14781.17) < 1
    assert abs(actual[0,1] - 24042.25) < 1
    assert abs(actual[1,1] - 14781.17) < 1
    assert abs(actual[0,2] - 24042.25) < 1
    assert abs(actual[1,2] - 14781.17) < 1


def test_world_to_image_withoutgeoid():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITHOUT_G)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    with pytest.raises(ValueError) as e_info:
        z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'height', 'height', nonadir=False)[2]
        shot.set_z_nadir(z_nadir)
        WorldImageShot(shot,cam).world_to_image(point_terrain, DATA_TYPE_Z, SHOT_TYPE_Z)


def test_world_to_image_sametypea():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITHOUT_G)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'height', 'height', nonadir=False)[2]
    shot.set_z_nadir(z_nadir)
    WorldImageShot(shot,cam).world_to_image(point_terrain, 'altitude', 'altitude')


def test_world_to_image_sametypewithl():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', nonadir=False)[2]
    shot.set_z_nadir(z_nadir)
    WorldImageShot(shot,cam).world_to_image(point_terrain, 'altitude', 'altitude')


def test_world_to_image_sametypewithl_withoutdtm():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = copy.copy(SHOT)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', nonadir=False)[2]
    shot.set_z_nadir(z_nadir)
    with pytest.raises(ValueError) as e_info:
        Dtm_singleton(None,None)
        WorldImageShot(shot,cam).world_to_image(point_terrain, 'altitude', 'altitude')


def test_world_to_image_sametypewithoutl():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',False)
    cam = CAM
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', nonadir=False)[2]
    shot.set_z_nadir(z_nadir)
    Dtm_singleton(None, None)
    WorldImageShot(shot,cam).world_to_image(point_terrain, 'altitude', 'altitude')


def test_world_to_image_approx():
    Dtm.clear()
    shot = copy.copy(SHOT)
    Proj_singleton(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    cam = CAM
    shot.set_param_eucli_shot(approx=True)
    actual = WorldImageShot(shot, cam).world_to_image(point_terrain, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0] - 24042.25), abs(actual[1] - 14781.17))
    assert abs(actual[0] - 24042.25) < 1
    assert abs(actual[1] - 14781.17) < 1