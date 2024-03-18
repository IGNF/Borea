"""
Script test for module shot_pos
"""
import numpy as np
from src.worksite.worksite import Worksite
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.transform_worksite.space_resection import SpaceResection
from src.datastruct.dtm import Dtm
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_co_points import read_co_points


def Dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def Proj_singleton(epsg, proj_list = None, path_geoid = None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, proj_list, path_geoid)


def test_shootings_position():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm("./dataset/MNT_France_25m_h_crop.tif", "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot()
    SpaceResection(work).space_resection_worksite()
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[0] - 814975.925) < 0.02
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[1] - 6283986.148) < 0.02
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[2] - 1771.280) < 0.02
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[0] - 814977.593) < 0.02
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[1] - 6283733.183) < 0.02
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[2] - 1771.519) < 0.02


def test_space_resection():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam","degree", True)
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
    Proj_singleton(2154, {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"]}, "./dataset/")
    Dtm_singleton("./dataset/MNT_France_25m_h_crop.tif", "height")
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]), 'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    work = Worksite("Test")
    work.add_camera('test_cam', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    actual_shot = SpaceResection(work).space_resection(shot)
    assert abs(actual_shot.pos_shot[0] - 814975.925) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283986.148) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1771.280) < 0.02


def test_take_obs():
    work = reader_orientation("./dataset/23FD1305_alt_test.OPK",
                              {"interval": [2, None],
                              "header": "N X Y Z O P K C",
                              "unit_angle": "degree",
                              "linear_alteration": True})
    work.set_proj(2154, "./dataset/proj.json", "./dataset")
    read_camera(["./dataset/Camera1.txt"], work)
    work.set_dtm("./dataset/MNT_France_25m_h_crop.tif", "height")
    work.set_param_shot()
    read_co_points(["./dataset/liaisons_test.mes"], work)
    actual_obs, actual_ptw = SpaceResection(work).take_obs(work.shots["23FD1305x00026_01306"])
    assert (actual_obs[:,0:3] == np.array([[3885.75, 6033.01,3896.99],[14969.14,16208.41,13858.47]])).all()
    assert (np.round(actual_ptw[:,0:3],0) == np.array([[814451,814574,814450],[6283601,6283532,6283665],[401,399,401]])).all()


def test_space_resection_othershot():
    work = reader_orientation("./test/data/dataset2/23FD1305_alt_2.OPK",
                              {"interval": [2, None],
                              "header": "N X Y Z O P K C",
                              "unit_angle": "degree",
                              "linear_alteration": True})
    work.set_proj(2154, "./dataset/proj.json", "./dataset")
    read_camera(["./dataset/Camera1.txt"], work)
    work.set_dtm("./dataset/MNT_France_25m_h_crop.tif", "height")
    work.set_param_shot()
    actual_shot = SpaceResection(work).space_resection(work.shots["23FD1305x00054_05677"])
    assert abs(actual_shot.pos_shot[0] - 833127.599) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283057.326) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1765.554) < 0.02


def test_space_resection_withcopoints():
    work = reader_orientation("./test/data/dataset2/23FD1305_alt_2.OPK",
                            {"interval": [2, None],
                            "header": "N X Y Z O P K C",
                            "unit_angle": "degree",
                            "linear_alteration": True})
    work.set_proj(2154, "./dataset/proj.json", "./dataset")
    read_camera(["./dataset/Camera1.txt"], work)
    work.set_dtm("./dataset/MNT_France_25m_h_crop.tif", "height")
    work.set_param_shot()
    read_co_points(["./test/data/dataset2/all_liaisons2.mes"], work)
    actual_shot = SpaceResection(work).space_resection(work.shots["23FD1305x00054_05677"])
    SpaceResection(work).space_resection_worksite()
    assert abs(work.shots["23FD1305x00054_05677"].pos_shot[0] - 833127.599) < 0.02
    assert abs(work.shots["23FD1305x00054_05677"].pos_shot[1] - 6283057.326) < 0.02
    assert abs(work.shots["23FD1305x00054_05677"].pos_shot[2] - 1765.554) < 0.02
    assert abs(work.shots["23FD1305x00027_01475"].pos_shot[0] - 815631.723) < 0.02
    assert abs(work.shots["23FD1305x00027_01475"].pos_shot[1] - 6278954.522) < 0.02
    assert abs(work.shots["23FD1305x00027_01475"].pos_shot[2] - 1762.738) < 0.02
