"""
Script test for module WorldImageWork
"""
# pylint: disable=import-error, missing-function-docstring
import numpy as np
from src.worksite.worksite import Worksite
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
LIST_GEOID = ["./dataset/fr_ign_RAF20.tif"]
TYPE_POINT = [3]
TYPE_CONTROL_POINT = [13]
ALL_POINT = []


def test_calculate_world_to_image_base():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  'cam_test', "degree", True, "opk")
    work.set_proj(2154, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('gcp_test', 'shot_test', np.array([24042.25, 14781.17]))
    work.add_gcp3d('gcp_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    WorldImageWork(work).calculate_world_to_image(TYPE_POINT)
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcp3d) == 1


def test_calculate_world_to_image_addpointunknow():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  'cam_test', "degree", True, "opk")
    work.set_proj(2154, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('gcp_test', 'shot_test', np.array([24042.25, 14781.17]))
    work.add_gcp3d('gcp_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('gcp_test_test', 3, np.array([0, 0, 0]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    WorldImageWork(work).calculate_world_to_image(TYPE_POINT)
    print("The print is normal")
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcp3d) == 1


def test_calculate_world_to_image_testcode():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  'cam_test', "degree", True, "opk")
    work.set_proj(2154, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('gcp_test', 'shot_test', np.array([24042.25, 14781.17]))
    work.add_gcp2d('gcp_test_test', 'shot_test', np.array([24042.25, 14781.17]))
    work.add_gcp3d('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('gcp_test_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    WorldImageWork(work).calculate_world_to_image(TYPE_CONTROL_POINT)
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcp3d) == 1


def test_calculate_world_to_image_testcodenone():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  'cam_test', "degree", True, "opk")
    work.set_proj(2154, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('gcp_test', 'shot_test', np.array([24042.25, 14781.17]))
    work.add_gcp2d('gcp_test_test', 'shot_test', np.array([24042.25, 14781.17]))
    work.add_gcp3d('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('gcp_test_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    WorldImageWork(work).calculate_world_to_image(ALL_POINT)
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][0] - 24042.25) < 1
    assert abs(work.shots['shot_test'].gcp3d['gcp_test'][1] - 14781.17) < 1
    assert len(work.shots['shot_test'].gcp3d) == 2
