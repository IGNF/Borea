"""
Script test for module shot_pos
"""
import numpy as np
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.shot_pos import space_resection
from src.datastruct.dtm import Dtm
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


def Dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def Proj_singleton(epsg, proj_list = None, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, proj_list, path_geoid)


def test_space_resection():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam","degree", True)
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    Dtm_singleton("./dataset/MNT_France_25m_h_crop.tif", "height")
    shot.set_param_eucli_shot()
    z_nadir = ImageWorldShot(shot).image_to_world(cam.ppax, cam.ppay, cam, 'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    actual_shot = space_resection(shot, cam, "height", "altitude")
    assert abs(actual_shot.pos_shot[0] - 814975.925) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283986.148) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1771.280) < 0.02
