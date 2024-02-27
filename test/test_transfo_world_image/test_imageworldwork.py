"""
Script test for module ImageWorldWork
"""
import numpy as np
from src.worksite.worksite import Worksite


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def test_calculate_image_world_by_intersection_onecop_multiimg():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_co_point('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_co_point('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_co_point('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_image_world_by_intersection()
    print(abs(work.co_pts_world['"1003"'][0] - 815601.510),abs(work.co_pts_world['"1003"'][1] - 6283629.280),abs(work.co_pts_world['"1003"'][2] - 54.960))
    assert abs(work.co_pts_world['"1003"'][0] - 815601.510) < 1
    assert abs(work.co_pts_world['"1003"'][1] - 6283629.280) < 1
    assert abs(work.co_pts_world['"1003"'][2] - 54.960) < 1


def test_calculate_image_world_by_intersection_onecopwithoneimg():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_co_point('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_co_point('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_co_point('"1004"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_image_world_by_intersection()
    assert len(list(work.co_pts_world)) == 1
    assert '"1003"' in work.co_pts_world.keys()
    assert not('"1004"' in work.co_pts_world.keys())


def test_calculate_image_world_by_intersection_withzeropoint():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.calculate_image_world_by_intersection()
    print("The print is normal")
    assert work.co_pts_world == {}


def test_calculate_image_world_by_intersection_allgipoint():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test","degree",True)
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_ground_img_pt('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_ground_img_pt('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_ground_img_pt('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_ground_img_pt('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_ground_img_pt('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_image_world_by_intersection("ground_img_pt")
    print(abs(work.img_pts_world['"1003"'][0] - 815601.510),abs(work.img_pts_world['"1003"'][1] - 6283629.280),abs(work.img_pts_world['"1003"'][2] - 54.960))
    print(abs(work.img_pts_world['"1005"'][0] - 833670.940),abs(work.img_pts_world['"1005"'][1] - 6281965.400),abs(work.img_pts_world['"1005"'][2] - 52.630))
    assert len(list(work.img_pts_world)) == 2
    assert '"1003"' in work.img_pts_world.keys()
    assert '"1005"' in work.img_pts_world.keys()
    assert abs(work.img_pts_world['"1003"'][0] - 815601.510) < 1
    assert abs(work.img_pts_world['"1003"'][1] - 6283629.280) < 1
    assert abs(work.img_pts_world['"1003"'][2] - 54.960) < 1


def test_calculate_image_world_by_intersection_gipoint13type():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test","degree",True)
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.add_ground_img_pt('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_ground_img_pt('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_ground_img_pt('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_ground_img_pt('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_ground_img_pt('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.add_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_z_nadir_shot()
    work.calculate_image_world_by_intersection("ground_img_pt", [13])
    assert len(list(work.img_pts_world)) == 1
    assert '"1003"' in work.img_pts_world.keys()
    assert '"1005"' not in work.img_pts_world.keys()


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
    work.set_z_nadir_shot()
    actual = work.intersection_pt_in_2shot('"1003"', work.shots["shot1"], work.shots["shot2"])
    print(abs(actual[0] - 815601.510),abs(actual[1] - 6283629.280),abs(actual[2] - 54.960))
    assert abs(actual[0] - 815601.510) < 1
    assert abs(actual[1] - 6283629.280) < 1
    assert abs(actual[2] - 54.960) < 1


def test_copoints_position():
    work = Worksite("Test")