"""
Script test for module statistics
"""
import os
import numpy as np
import shutil as shutil
from src.datastruct.worksite import Worksite
from src.stat.statistics import Stat


OUTPUT = "./test/tmp"
FILENAME = "Test"

def setup_module(module): # run before the first test
    try:  # Clean folder test if exists
        shutil.rmtree(OUTPUT)
    except FileNotFoundError:
        pass
    os.makedirs(OUTPUT, exist_ok=True)


def test_stat_world_to_image():
    work = Worksite(FILENAME)
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.check_gip = True
    work.add_gcp('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.check_gcp = True
    work.calculate_world_to_image_gcp([13])
    stat = Stat(work, "./", [13])
    stat.stat_world_to_image()
    assert stat.res_world_image[0][0][0] == 'gcp_test'
    assert stat.res_world_image[0][0][1] == 'shot_test'
    assert np.all(stat.res_world_image[0][1] == np.array([2.990902358244057, 2.167273693090465]))
    assert len(stat.res_world_image) == 1


def test_stat_world_to_image_withoutdata():
    work = Worksite(FILENAME)
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.check_gip = True
    work.add_gcp('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.check_gcp = True
    stat = Stat(work, "./", [13])
    stat.stat_world_to_image()
    assert stat.res_world_image == []
    assert stat.check_stat_wi == False


def test_stat_image_to_world_type13():
    work = Worksite(FILENAME)
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test")
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test")
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_gipoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_gipoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_gipoint('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_gipoint('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.check_gip = True
    work.check_gcp = True
    work.calculate_init_image_world("gipoint")
    stat = Stat(work, "./", [13])
    stat.stat_image_to_world()
    assert stat.res_image_world[0][0][0] == '"1003"'
    assert np.all(np.round(stat.res_image_world[0][1],2) == np.round(np.array([15.479717904701829,-223.1927813924849,-3456.2759610545118]),2))
    assert len(stat.res_image_world) == 1


def test_stat_image_to_world_alltype():
    work = Worksite(FILENAME)
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test")
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test")
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_gipoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_gipoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_gipoint('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_gipoint('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.check_gip = True
    work.check_gcp = True
    work.calculate_init_image_world("gipoint")
    stat = Stat(work, "./", [])
    stat.stat_image_to_world()
    assert stat.res_image_world[0][0][0] == '"1003"'
    assert np.all(np.round(stat.res_image_world[0][1],2) == np.round(np.array([15.479717904701829,-223.1927813924849,-3456.2759610545118]),2))
    assert stat.res_image_world[1][0][0] == '"1005"'
    assert np.all(np.round(stat.res_image_world[1][1],2) == np.round(np.array([4.70253158127889,-426.9300078107044,-3462.877340453979]),2))
    assert len(stat.res_image_world) == 2


def test_stat_image_to_world_withoutdata():
    work = Worksite(FILENAME)
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.check_gip = True
    work.add_gcp('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.check_gcp = True
    stat = Stat(work, "./", [13])
    stat.stat_image_to_world()
    assert stat.res_image_world == []
    assert stat.check_stat_iw == False


def test_stat_list_world1():
    work = Worksite(FILENAME)
    stat = Stat(work, "./", [])
    list_data = [[["p1"], np.array([1,1,1])],
                 [["p2"], np.array([3,0,4])],
                 [["p3"], np.array([2,2,2])],
                 [["p4"], np.array([10,12,6])],
                 [["p5"], np.array([-13,-2,-1])]]
    dict_stat = stat.stat_list(list_data)
    assert np.all(dict_stat["Min_arith"]["val"] == np.array([-13,-2,-1]))
    assert np.all(dict_stat["Min_abs"]["val"] == np.array([1,0,1]))
    assert np.all(dict_stat["Max_arith"]["val"] == np.array([10,12,6]))
    assert np.all(dict_stat["Max_abs"]["val"] == np.array([13,12,6]))
    assert np.all(dict_stat["Mean_arith"] == np.array([0.6,2.6,2.4]))
    assert np.all(dict_stat["Mean_abs"]== np.array([5.8,3.4,2.8]))
    assert np.all(dict_stat["Median_arith"] == np.array([2,1,2]))
    assert np.all(dict_stat["Median_abs"] == np.array([3,2,2]))
    assert np.all(dict_stat["Var_arith"] == np.array([56.24,23.84,5.84]))
    assert np.all(dict_stat["Var_abs"] == np.array([22.96,19.04,3.76]))
    assert np.all(dict_stat["Sigma_arith"] == np.array([7.5,4.88,2.42]))
    assert np.all(dict_stat["Sigma_abs"] == np.array([4.79,4.36,1.94]))
    assert np.all(dict_stat["Min_arith"]["data"] == ["p5","p5","p5"])
    assert np.all(dict_stat["Min_abs"]["data"] == ["p1","p2","p1"])
    assert np.all(dict_stat["Max_arith"]["data"] == ["p4","p4","p4"])
    assert np.all(dict_stat["Max_abs"]["data"] == ["p5","p4","p4"])


def test_stat_list_image1():
    work = Worksite(FILENAME)
    stat = Stat(work, "./", [])
    list_data = [[["p1", "s1"], np.array([1,1])],
                 [["p2", "s2"], np.array([3,0])],
                 [["p3", "s3"], np.array([2,2])],
                 [["p4", "s4"], np.array([10,12])],
                 [["p5", "s5"], np.array([-13,-2])]]
    dict_stat = stat.stat_list(list_data)
    assert np.all(dict_stat["Min_arith"]["val"] == np.array([-13,-2]))
    assert np.all(dict_stat["Min_abs"]["val"] == np.array([1,0]))
    assert np.all(dict_stat["Max_arith"]["val"] == np.array([10,12]))
    assert np.all(dict_stat["Max_abs"]["val"] == np.array([13,12]))
    assert np.all(dict_stat["Mean_arith"] == np.array([0.6,2.6]))
    assert np.all(dict_stat["Mean_abs"]== np.array([5.8,3.4]))
    assert np.all(dict_stat["Median_arith"] == np.array([2,1]))
    assert np.all(dict_stat["Median_abs"] == np.array([3,2]))
    assert np.all(dict_stat["Var_arith"] == np.array([56.24,23.84]))
    assert np.all(dict_stat["Var_abs"] == np.array([22.96,19.04]))
    assert np.all(dict_stat["Sigma_arith"] == np.array([7.5,4.88]))
    assert np.all(dict_stat["Sigma_abs"] == np.array([4.79,4.36]))
    assert np.all(dict_stat["Min_arith"]["data"] == [["p5","s5"],["p5","s5"]])
    assert np.all(dict_stat["Min_abs"]["data"] == [["p1","s1"],["p2","s2"]])
    assert np.all(dict_stat["Max_arith"]["data"] == [["p4","s4"],["p4","s4"]])
    assert np.all(dict_stat["Max_abs"]["data"] == [["p5","s5"],["p4","s4"]])


def test_stat_list_world2():
    work = Worksite(FILENAME)
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test")
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test")
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_gipoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_gipoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_gipoint('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_gipoint('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.check_gip = True
    work.check_gcp = True
    work.calculate_init_image_world("gipoint")
    stat = Stat(work, "./", [])
    stat.stat_image_to_world()
    dict_stat = stat.stat_list(stat.res_image_world)
    assert len(dict_stat.keys()) == 12
    

def test_stat_list_image2():
    work = Worksite(FILENAME)
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test")
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test")
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_gipoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_gipoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_gipoint('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_gipoint('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.check_gip = True
    work.check_gcp = True
    work.calculate_world_to_image_gcp([])
    stat = Stat(work, "./", [])
    stat.stat_world_to_image()
    dict_stat = stat.stat_list(stat.res_world_image)
    assert len(dict_stat.keys()) == 12


def test_save_txt():
    work = Worksite(FILENAME)
    stat = Stat(work, OUTPUT, [])
    stat.res_image_world = [[["p1"], np.array([1,1,1])],
                            [["p2"], np.array([3,0,4])],
                            [["p3"], np.array([2,2,2])],
                            [["p4"], np.array([10,12,6])],
                            [["p5"], np.array([-13,-2,-1])]]
    stat.res_world_image = [[["p1", "s1"], np.array([1,1])],
                            [["p2", "s2"], np.array([3,0])],
                            [["p3", "s3"], np.array([2,2])],
                            [["p4", "s4"], np.array([10,12])],
                            [["p5", "s5"], np.array([-13,-2])]]
    stat.stat_world_image = stat.stat_list(stat.res_world_image)
    stat.stat_image_world = stat.stat_list(stat.res_image_world)
    stat.save_stat_txt()
    assert os.path.exists(f"{OUTPUT}/Stat_{FILENAME}.txt")


def test_main():
    work = Worksite(FILENAME)
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.add_shot("23FD1305x00054_05680",np.array([833124.675,6282303.066,1761.305]),np.array([-0.198514051868,-0.023898399551,0.190559923925]),"cam_test")
    work.add_shot("23FD1305x00054_05681",np.array([833123.958,6282051.774,1761.056]),np.array([-0.222610811997,-0.045739865938,0.163818133681]),"cam_test")
    work.set_proj("2154", "test/data/proj.json", "./test/data/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_gipoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_gipoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_gipoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.add_gipoint('"1005"',"23FD1305x00054_05680",22796.05,14371.27)
    work.add_gipoint('"1005"',"23FD1305x00054_05681",22817.4,9930.73)
    work.add_gcp('"1003"',13,np.array([815601.510,6283629.280,54.960]))
    work.add_gcp('"1005"',3,np.array([833670.940,6281965.400,52.630]))
    work.check_gip = True
    work.check_gcp = True
    work.calculate_world_to_image_gcp([])
    work.calculate_init_image_world("gipoint")
    stat = Stat(work, OUTPUT, [])
    stat.main_stat_and_save()
    assert os.path.exists(f"{OUTPUT}/Stat_{FILENAME}.txt")
