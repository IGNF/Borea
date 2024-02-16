"""
Script test for module shot
"""
import pytest
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj
from src.altimetry.dem import Dem

SHOT = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True)
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
EPSG = "EPSG:2154"
DICT_PROJ_WITH_G = {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}
DICT_PROJ_WITHOUT_G = {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'}
PATH_GEOID = "./dataset/"
PATH_DEM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "h"
SHOT_TYPE_Z = "al"


def test_set_param_eucli():
    shot = SHOT
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(proj)
    pos_expected = projeucli.world_to_euclidean(814975.925, 6283986.148, 1771.280)
    assert np.all(shot.pos_shot_eucli == pos_expected)


def test_set_param_eucli_withoutdem():
    shot = SHOT
    proj = ProjEngine(EPSG, DICT_PROJ_WITHOUT_G)
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(proj)
    pos_expected = projeucli.world_to_euclidean(814975.925, 6283986.148, 1771.280)
    assert np.all(shot.pos_shot_eucli == pos_expected)


def test_from_shot_eucli():
    shot = SHOT
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    shot.set_param_eucli_shot(proj)
    shot_eucli = Shot.from_param_euclidean("test_shot", shot.pos_shot_eucli, shot.mat_rot_eucli, "test_cam", "degree",True, proj)
    assert shot.name_shot == shot_eucli.name_shot
    assert shot.pos_shot[0] == round(shot_eucli.pos_shot[0],3)
    assert shot.pos_shot[1] == round(shot_eucli.pos_shot[1],3)
    assert shot.pos_shot[2] == round(shot_eucli.pos_shot[2],3)
    assert round(shot.ori_shot[0],3) == round(shot_eucli.ori_shot[0],3)
    assert round(shot.ori_shot[1],3) == round(shot_eucli.ori_shot[1],3)
    assert round(shot.ori_shot[2],3) == round(shot_eucli.ori_shot[2],3)
    assert round(shot.ori_shot_eucli[0],3) == round(shot_eucli.ori_shot_eucli[0],3)
    assert round(shot.ori_shot_eucli[1],3) == round(shot_eucli.ori_shot_eucli[1],3)
    assert round(shot.ori_shot_eucli[2],3) == round(shot_eucli.ori_shot_eucli[2],3)


def test_world_to_image():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    dem = Dem(PATH_DEM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(proj)
    actual = shot.world_to_image(point_terrain[0], point_terrain[1], point_terrain[2], cam, dem, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0] - 24042.25), abs(actual[1] - 14781.17))
    assert abs(actual[0] - 24042.25) < 1
    assert abs(actual[1] - 14781.17) < 1


def test_world_to_image_withoutgeoid():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITHOUT_G)
    dem = None
    shot.set_param_eucli_shot(proj)
    with pytest.raises(ValueError) as e_info:
        shot.world_to_image(point_terrain[0], point_terrain[1], point_terrain[2], cam, dem, DATA_TYPE_Z, SHOT_TYPE_Z)


def test_world_to_image_sametypea():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITHOUT_G)
    dem = None
    shot.set_param_eucli_shot(proj)
    shot.world_to_image(point_terrain[0], point_terrain[1], point_terrain[2], cam, dem, 'a', 'a')


def test_world_to_image_sametypewithl():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    dem = None
    shot.set_param_eucli_shot(proj)
    shot.world_to_image(point_terrain[0], point_terrain[1], point_terrain[2], cam, dem, 'al', 'hl')


def test_world_to_image_sametypewithoutl():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    dem = None
    shot.set_param_eucli_shot(proj)
    shot.world_to_image(point_terrain[0], point_terrain[1], point_terrain[2], cam, dem, 'h', 'a')


def test_image_to_world():
    point_image = np.array([24042.25, 14781.17])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    dem = Dem(PATH_DEM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(proj)
    actual = shot.image_to_world(point_image[0], point_image[1], cam, dem, DATA_TYPE_Z, SHOT_TYPE_Z)
    print(abs(actual[0] - 815601.510),abs(actual[1] - 6283629.280),abs(actual[2] - 54.960))
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 3


def test_image_to_world_sametype_withoutgeoid():
    point_image = np.array([24042.25, 14781.17])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITHOUT_G)
    dem = Dem(PATH_DEM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(proj)
    actual = shot.image_to_world(point_image[0], point_image[1], cam, dem, DATA_TYPE_Z, DATA_TYPE_Z)


def test_image_to_world_withoutdem():
    point_image = np.array([24042.25, 14781.17])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    dem = None
    shot.set_param_eucli_shot(proj)
    with pytest.raises(ValueError) as e_info:
        actual = shot.image_to_world(point_image[0], point_image[1], cam, dem, DATA_TYPE_Z, SHOT_TYPE_Z)


def test_image_to_world_multipoint():
    c = np.array([24042.25, 24042.25])
    l = np.array([14781.17, 14781.17])
    shot = SHOT
    cam = CAM
    proj = ProjEngine(EPSG, DICT_PROJ_WITH_G, PATH_GEOID)
    dem = Dem(PATH_DEM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(proj)
    actual = shot.image_to_world(c, l, cam, dem, DATA_TYPE_Z, SHOT_TYPE_Z)
    assert abs(actual[0,0] - 815601.510) < 1
    assert abs(actual[1,0] - 6283629.280) < 1
    assert abs(actual[2,0] - 54.960) < 3
