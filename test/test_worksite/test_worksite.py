"""
Script test for module worksite
"""
import numpy as np
from src.worksite.worksite import Worksite

PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def test_barycentre():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_shot("shot2", np.array([3,6,6]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_shot("shot3", np.array([2,8,10]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_shot("shot4", np.array([2,10,14]), np.array([1,1,1]), 'cam_test',"degree",True)
    bary = work.calculate_barycentre()
    assert bary[0] == 2
    assert bary[1] == 8
    assert bary[2] == 8


def test_shootings_position():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.shootings_position()
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[0] - 814975.925) < 5
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[1] - 6283986.148) < 5
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[2] - 1771.280) < 5
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[0] - 814977.593) < 5
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[1] - 6283733.183) < 5
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[2] - 1771.519) < 5