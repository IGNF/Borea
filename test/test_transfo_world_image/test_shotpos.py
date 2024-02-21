"""
Script test for module shot_pos
"""
import numpy as np
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.shot_pos import space_resection
from src.datastruct.dtm import Dtm


def Dtm_singleton(path, type_dtm):
        Dtm().set_dtm(path, type_dtm)


def test_space_resection():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam","degree", True)
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    proj = ProjEngine(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    Dtm_singleton("./dataset/MNT_France_25m_h_crop.tif", "h")
    shot.set_param_eucli_shot(proj)
    actual_shot = space_resection(shot, cam, proj, "h", "al")
    assert abs(actual_shot.pos_shot[0] - 814975.925) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283986.148) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1771.280) < 0.02
