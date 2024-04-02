"""
Script test for module workshot
"""
import pytest
import pyproj
import numpy as np
from src.worksite.worksite import Worksite
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def setup_module(module): # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_set_param_shot():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.set_proj(2154, ["./dataset/fr_ign_RAF20.tif"])
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.set_param_shot()
    assert (work.shots["shot1"].pos_shot_eucli != None).all()
    assert work.shots["shot1"].z_nadir != None


def test_set_param_shot_noprojengineandtypediff():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.set_proj(4339)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    with pytest.raises(ValueError) as e_info:
        work.set_param_shot()


def test_set_param_shot_noprojengineandsametype():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.set_proj(4339)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "height"
    work.type_z_data = "height"
    with pytest.raises(ValueError) as e_info:
        work.set_param_shot()


def test_set_param_shot_nodtm():
    Dtm.clear()
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.set_proj(2154, ["./dataset/fr_ign_RAF20.tif"])
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_param_shot()
    assert (work.shots["shot1"].pos_shot_eucli != None).all()
    assert work.shots["shot1"].z_nadir == None


def test_set_unit_shot():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.set_proj(2154, ["./dataset/fr_ign_RAF20.tif"])
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.set_param_shot(approx=False)
    work.set_unit_shot("height", "radian", linear_alteration=False)
    assert work.shots["shot1"].unit_angle == "radian"
    assert work.shots["shot1"].linear_alteration == False
    assert (work.shots["shot1"].ori_shot == np.array([np.pi,0,2*np.pi])).all()
    assert work.type_z_shot == "height"


def test_set_unit_shot_sameunit():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_unit_shot("altitude", "degree", linear_alteration=True)
    assert work.shots["shot1"].unit_angle == "degree"
    assert work.shots["shot1"].linear_alteration == True
    assert (work.shots["shot1"].ori_shot == np.array([180,0,360])).all()
    assert work.type_z_shot == "altitude"


def test_set_unit_shot_changeorder():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True,'opk')
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_unit_shot(order_axe="pok")
    assert (work.shots["shot1"].ori_shot != np.array([180,0,360])).all()
