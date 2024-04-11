"""
Module to test ConversionZ
"""
from pathlib import Path, PureWindowsPath
import numpy as np
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.dtm import Dtm
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data, conv_output_z_type
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925,6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True,'opk')
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
EPSG = 2154
LIST_GEOID = ["./dataset/fr_ign_RAF20.tif"]
LIST_NO_GEOID = None
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "height"
SHOT_TYPE_Z = "altitude"


def Dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def Proj_singleton(epsg, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, path_geoid)


def test_conv_z_shot_to_z_data():
    shot = SHOT
    cam = CAM
    Proj_singleton(EPSG, LIST_GEOID)
    Dtm_singleton(PATH_DTM,DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot,cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    pos_new_z = conv_z_shot_to_z_data(shot, SHOT_TYPE_Z, DATA_TYPE_Z)
    assert round(pos_new_z[2],0) == 1820


def test_conv_output_z_type():
    x = [814975.925,6283986.148,1771.280]
    Proj_singleton(EPSG, LIST_GEOID)
    new_x = conv_output_z_type(x,SHOT_TYPE_Z, DATA_TYPE_Z)
    assert round(new_x[2],0) == 1821
