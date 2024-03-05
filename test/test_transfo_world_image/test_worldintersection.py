"""
Test module for World Intersection
"""
import numpy as np
from src.worksite.worksite import Worksite
from src.transform_world_image.transform_worksite.image_world_intersection import WorldIntersection


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def test_eucli_intersection_2p():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("shot2",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_co_point('"1003"',"shot1",24042.25,14781.17)
    work.add_co_point('"1003"',"shot2",24120.2,10329.3)
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(False)
    actual = WorldIntersection(work).intersection_pt_in_2shot('"1003"', work.shots["shot1"], work.shots["shot2"])
    print(abs(actual[0] - 815601.510),abs(actual[1] - 6283629.280),abs(actual[2] - 54.960))
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 1
