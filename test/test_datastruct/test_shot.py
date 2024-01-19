"""
Script test for module shot
"""
import pytest
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


def test_set_param_eucli():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    pos_expected = projeucli.world_to_euclidean(814975.925, 6283986.148, 1771.280)
    assert np.all(shot.pos_shot_eucli == pos_expected)


def test_set_param_eucli_withoutgeoid():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    assert shot.z_alti == None


def test_from_shot_eucli():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    shot_eucli = Shot.from_param_euclidean("test_shot", shot.pos_shot_eucli, shot.mat_rot_eucli, "test_cam", projeucli)
    assert shot.name_shot == shot_eucli.name_shot
    assert shot.pos_shot[0] == round(shot_eucli.pos_shot[0],3)
    assert shot.pos_shot[1] == round(shot_eucli.pos_shot[1],3)
    assert shot.pos_shot[2] == round(shot_eucli.pos_shot[2],3)


def test_world_to_image():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    actual = shot.world_to_image(point_terrain, cam, projeucli)
    assert abs(actual[0] - 24042.25) < 5
    assert abs(actual[1] - 14781.17) < 5


def test_world_to_image_array():
    x_world = np.array([815601.510, 815601.510, 815601.510])
    y_world = np.array([6283629.280, 6283629.280, 6283629.280])
    z_world = np.array([54.960, 54.960, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual = shot.world_to_image(x_world, y_world, z_world, cam, projeucli)
    assert abs(actual[0,0] - 24042.25) < 5
    assert abs(actual[1,0] - 14781.17) < 5


def test_world_to_image_withoutgeoid():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    with pytest.raises(AttributeError) as e_info:
        shot.world_to_image(point_terrain[0], point_terrain[1], point_terrain[2], cam, projeucli)


def test_image_to_world_float():
    point_image = np.array([24042.25, 14781.17])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    actual = shot.image_to_world(point_image[0],point_image[1],cam,projeucli,54.960)
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 1


def test_image_to_world_array():
    col = np.array([24042.25, 24042.25])
    line = np.array([14781.17, 14781.17])
    z = np.array([54.960, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual = shot.image_to_world(col,line,cam,projeucli,z)
    assert abs(actual[0,0] - 815601.510) < 1
    assert abs(actual[1,0] - 6283629.280) < 1
    assert abs(actual[2,0] - 54.960) < 1


def test_image_to_world_withoutgeoid():
    point_image = np.array([24042.25, 14781.17])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    shot.set_param_eucli_shot(projeucli)
    with pytest.raises(AttributeError) as e_info:
        actual = shot.image_to_world(point_image[0],point_image[1],cam,projeucli,54.960)