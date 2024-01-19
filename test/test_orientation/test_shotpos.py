"""
Script test for module shot_pos
"""
import numpy as np
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj
from src.geodesy.proj_engine import ProjEngine
from src.orientation.shot_pos import shooting_position


def test_shooting_position():
    shot = Shot("test_shot", np.array([814980, 6283990,1770]), np.array([0,0,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    cam.add_dim_image(26460.00, 17004.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual_shot = shooting_position(shot, cam, projeucli)
    print(abs(actual_shot.pos_shot[0] - 814975.925), abs(actual_shot.pos_shot[1] - 6283986.148), abs(actual_shot.pos_shot[2] - 1771.280))
    assert abs(actual_shot.pos_shot[0] - 814975.925) < 1000
    assert abs(actual_shot.pos_shot[1] - 6283986.148) < 1000
    assert abs(actual_shot.pos_shot[2] - 1771.280) < 1000
