"""
Script test for module shot
"""
import pytest
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


def test_world_to_image():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual = shot.world_to_image(point_terrain, cam, projeucli)
    assert abs(actual[0] - 24042.25) < 5
    assert abs(actual[1] - 14781.17) < 5


def test_world_to_image_withoutgeoid():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    with pytest.raises(AttributeError) as e_info:
        shot.world_to_image(point_terrain, cam, projeucli)


def test_image_to_world():
    point_image = np.array([24042.25, 14781.17])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual = shot.image_to_world(point_image[0],point_image[1],cam,projeucli,54.960)
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 1


def test_image_to_world_withoutgeoid():
    point_image = np.array([24042.25, 14781.17])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    with pytest.raises(AttributeError) as e_info:
        actual = shot.image_to_world(point_image[0],point_image[1],cam,projeucli,54.960)
