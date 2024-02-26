"""
Script test for module WorldImageWork
"""
import numpy as np
from src.worksite.worksite import Worksite


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def test_calculate_world_to_image_base():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test',"degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_ground_img_pt('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.add_gcp('gcp_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_world_to_image([3])
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcps) == 1


def test_calculate_world_to_image_addpointunknow():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test',"degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_ground_img_pt('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.add_gcp('gcp_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp('gcp_test_test', 3, np.array([0,0,0]))
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_world_to_image([3])
    print("The print is normal")
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcps) == 1


def test_calculate_world_to_image_testcode():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test',"degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_ground_img_pt('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.add_ground_img_pt('gcp_test_test', 'shot_test', 24042.25, 14781.17)
    work.add_gcp('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp('gcp_test_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_world_to_image([13])
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcps) == 1


def test_calculate_world_to_image_testcodeNone():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test',"degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_ground_img_pt('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.add_ground_img_pt('gcp_test_test', 'shot_test', 24042.25, 14781.17)
    work.add_gcp('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp('gcp_test_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_world_to_image([])
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcps) == 2