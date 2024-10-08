"""
Module to test ConversionZ
"""
# pylint: disable=import-error, missing-function-docstring, duplicate-code
import numpy as np
from borea.datastruct.shot import Shot
from borea.datastruct.camera import Camera
from borea.datastruct.dtm import Dtm
from borea.geodesy.proj_engine import ProjEngine
from borea.transform_world_image.transform_shot.conversion_coor_shot import conv_z_shot_to_z_data
from borea.transform_world_image.transform_shot.conversion_coor_shot import conv_output_z_type
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot


SHOT = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
            np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
            "test_cam", 'degree', True, 'opk')
CAM = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
EPSG = [2154]
LIST_GEOID = ["./dataset/fr_ign_RAF20.tif"]
LIST_NO_GEOID = None
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
DATA_TYPE_Z = "height"
SHOT_TYPE_Z = "altitude"


def dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def proj_singleton(epsg, path_geoid=None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, path_geoid)


def test_conv_z_shot_to_z_data():
    shot = SHOT
    cam = CAM
    proj_singleton(EPSG, LIST_GEOID)
    dtm_singleton(PATH_DTM, DATA_TYPE_Z)
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    pos_new_z = conv_z_shot_to_z_data(shot, SHOT_TYPE_Z, DATA_TYPE_Z)
    assert round(pos_new_z[2], 0) == 1820


def test_conv_output_z_type():
    x = [814975.925, 6283986.148, 1771.280]
    proj_singleton(EPSG, LIST_GEOID)
    new_x = conv_output_z_type(x, SHOT_TYPE_Z, DATA_TYPE_Z)
    assert round(new_x[2], 0) == 1821
