"""
Script test for module ImageWorldWork
"""
# pylint: disable=import-error, missing-function-docstring, duplicate-code
import numpy as np
from borea.worksite.worksite import Worksite
from borea.transform_world_image.transform_worksite.image_world_work import ImageWorldWork


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
EPSG = [2154]
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]


def test_calculate_image_world_by_intersection_onecop_multiimg():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_co_point('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_co_point('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_co_point('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_process="inter")
    print(abs(work.co_pts_world['"1003"'][0] - 815601.510),
          abs(work.co_pts_world['"1003"'][1] - 6283629.280),
          abs(work.co_pts_world['"1003"'][2] - 54.960))
    assert abs(work.co_pts_world['"1003"'][0] - 815601.510) < 1
    assert abs(work.co_pts_world['"1003"'][1] - 6283629.280) < 1
    assert abs(work.co_pts_world['"1003"'][2] - 54.960) < 1


def test_calculate_image_world_by_least_square_onecop_multiimg():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_co_point('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_co_point('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_co_point('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_process="square")
    print(abs(work.co_pts_world['"1003"'][0] - 815601.510),
          abs(work.co_pts_world['"1003"'][1] - 6283629.280),
          abs(work.co_pts_world['"1003"'][2] - 54.960))
    assert abs(work.co_pts_world['"1003"'][0] - 815601.510) < 0.2
    assert abs(work.co_pts_world['"1003"'][1] - 6283629.280) < 0.1
    assert abs(work.co_pts_world['"1003"'][2] - 54.960) < 0.6


def test_calculate_image_world_by_leastsquare_allgipoint():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05680", np.array([833124.675, 6282303.066, 1761.305]),
                  np.array([-0.198514051868, -0.023898399551, 0.190559923925]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05681", np.array([833123.958, 6282051.774, 1761.056]),
                  np.array([-0.222610811997, -0.045739865938, 0.163818133681]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05680", np.array([22796.05, 14371.27]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05681", np.array([22817.4, 9930.73]))
    work.add_gcp3d('"1003"', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('"1005"', 3, np.array([833670.940, 6281965.400, 52.630]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_point="gcp2d", type_process="square")
    print(abs(work.gcp2d_in_world['"1003"'][0] - 815601.510),
          abs(work.gcp2d_in_world['"1003"'][1] - 6283629.280),
          abs(work.gcp2d_in_world['"1003"'][2] - 54.960))
    print(abs(work.gcp2d_in_world['"1005"'][0] - 833670.940),
          abs(work.gcp2d_in_world['"1005"'][1] - 6281965.400),
          abs(work.gcp2d_in_world['"1005"'][2] - 52.630))
    assert len(list(work.gcp2d_in_world)) == 2
    assert '"1003"' in work.gcp2d_in_world.keys()
    assert '"1005"' in work.gcp2d_in_world.keys()
    assert abs(work.gcp2d_in_world['"1003"'][0] - 815601.510) < 2
    assert abs(work.gcp2d_in_world['"1003"'][1] - 6283629.280) < 1
    assert abs(work.gcp2d_in_world['"1003"'][2] - 54.960) < 3


def test_calculate_image_world_by_leastsquare_gipoint13type():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05680", np.array([833124.675, 6282303.066, 1761.305]),
                  np.array([-0.198514051868, -0.023898399551, 0.190559923925]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05681", np.array([833123.958, 6282051.774, 1761.056]),
                  np.array([-0.222610811997, -0.045739865938, 0.163818133681]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05680", np.array([22796.05, 14371.27]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05681", np.array([22817.4, 9930.73]))
    work.add_gcp3d('"1003"', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('"1005"', 3, np.array([833670.940, 6281965.400, 52.630]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_point="gcp2d", type_process="square",
                                            control_type=[13])
    assert len(list(work.gcp2d_in_world)) == 1
    assert '"1003"' in work.gcp2d_in_world.keys()
    assert '"1005"' not in work.gcp2d_in_world.keys()


def test_calculate_image_world_by_intersection_onecopwithoneimg():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_co_point('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_co_point('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_co_point('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_process="inter")
    assert len(list(work.co_pts_world)) == 1
    assert '"1003"' in work.co_pts_world.keys()
    assert '"1004"' not in work.co_pts_world.keys()


def test_calculate_image_world_by_intersection_withzeropoint():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    ImageWorldWork(work).manage_image_world(type_process="inter")
    assert work.co_pts_world == {}


def test_calculate_image_world_by_intersection_allgipoint():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05680", np.array([833124.675, 6282303.066, 1761.305]),
                  np.array([-0.198514051868, -0.023898399551, 0.190559923925]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05681", np.array([833123.958, 6282051.774, 1761.056]),
                  np.array([-0.222610811997, -0.045739865938, 0.163818133681]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05680", np.array([22796.05, 14371.27]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05681", np.array([22817.4, 9930.73]))
    work.add_gcp3d('"1003"', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('"1005"', 3, np.array([833670.940, 6281965.400, 52.630]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_point="gcp2d", type_process="inter")
    print(abs(work.gcp2d_in_world['"1003"'][0] - 815601.510),
          abs(work.gcp2d_in_world['"1003"'][1] - 6283629.280),
          abs(work.gcp2d_in_world['"1003"'][2] - 54.960))
    print(abs(work.gcp2d_in_world['"1005"'][0] - 833670.940),
          abs(work.gcp2d_in_world['"1005"'][1] - 6281965.400),
          abs(work.gcp2d_in_world['"1005"'][2] - 52.630))
    assert len(list(work.gcp2d_in_world)) == 2
    assert '"1003"' in work.gcp2d_in_world.keys()
    assert '"1005"' in work.gcp2d_in_world.keys()
    assert abs(work.gcp2d_in_world['"1003"'][0] - 815601.510) < 1
    assert abs(work.gcp2d_in_world['"1003"'][1] - 6283629.280) < 1
    assert abs(work.gcp2d_in_world['"1003"'][2] - 54.960) < 1


def test_calculate_image_world_by_intersection_gipoint13type():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05680", np.array([833124.675, 6282303.066, 1761.305]),
                  np.array([-0.198514051868, -0.023898399551, 0.190559923925]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00054_05681", np.array([833123.958, 6282051.774, 1761.056]),
                  np.array([-0.222610811997, -0.045739865938, 0.163818133681]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(EPSG, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.add_gcp2d('"1003"', "23FD1305x00026_01306", np.array([24042.25, 14781.17]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01307", np.array([24120.2, 10329.3]))
    work.add_gcp2d('"1003"', "23FD1305x00026_01308", np.array([24161.49, 5929.37]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05680", np.array([22796.05, 14371.27]))
    work.add_gcp2d('"1005"', "23FD1305x00054_05681", np.array([22817.4, 9930.73]))
    work.add_gcp3d('"1003"', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('"1005"', 3, np.array([833670.940, 6281965.400, 52.630]))
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    ImageWorldWork(work).manage_image_world(type_point="gcp2d", type_process="inter",
                                            control_type=[13])
    assert len(list(work.gcp2d_in_world)) == 1
    assert '"1003"' in work.gcp2d_in_world.keys()
    assert '"1005"' not in work.gcp2d_in_world.keys()
