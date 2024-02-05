"""
Script test for module shot_pos
"""
import numpy as np
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.euclidean_proj import EuclideanProj
from src.geodesy.proj_engine import ProjEngine
from src.position.shot_pos import space_resection


def test_space_resection():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20_test"]}, "./test/data/")
    shot.set_param_eucli_shot(proj)
    actual_shot = space_resection(shot, cam, proj)
    assert abs(actual_shot.pos_shot[0] - 814975.925) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283986.148) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1771.280) < 0.02
