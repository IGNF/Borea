"""
Script test for function classes
"""
import numpy as np
from src.datastruct.worksite import Worksite
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.gcp import GCP
from src.geodesy.proj_engine import ProjEngine
from src.geodesy.euclidean_proj import EuclideanProj


def test_add_shot():
    obj = Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    assert obj.shots["test_shot"].name_shot == "test_shot"
    assert obj.shots["test_shot"].pos_shot[0] == 1
    assert obj.shots["test_shot"].pos_shot[1] == 2
    assert obj.shots["test_shot"].pos_shot[2] == 3
    assert obj.shots["test_shot"].ori_shot[0] == 3
    assert obj.shots["test_shot"].ori_shot[1] == 2
    assert obj.shots["test_shot"].ori_shot[2] == 1
    assert obj.shots["test_shot"].name_cam == "test_cam"


def test_set_proj_1():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:2154")
    assert work.proj.projection_list == {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', 'comment': 'Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93'}
    assert work.projeucli.x_central == 1
    assert work.projeucli.y_central == 2


def test_set_proj_2():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:4339", "test/data/proj.json")
    assert work.proj.projection_list == {"geoc": "EPSG:4340", "geog": "EPSG:4176", "comment": "Projection of Australian Antartic"}
    assert work.projeucli.x_central == 1
    assert work.projeucli.y_central == 2


def test_set_proj_3():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:4339")
    assert work.proj.epsg == "EPSG:4339"


def test_set_proj_4():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:4326", "test/data/proj.json")
    assert work.proj.epsg == "EPSG:4326"


def test_add_cam():
    obj = Worksite(name = "Test")
    obj.add_camera("test_cam", 13210.00, 8502.00, 30975.00)
    assert obj.cameras["test_cam"].name_camera == "test_cam"
    assert obj.cameras["test_cam"].ppax == 13210.00
    assert obj.cameras["test_cam"].ppay == 8502.00
    assert obj.cameras["test_cam"].focal == 30975.00


def test_add_copoint():
    obj = Worksite(name = "Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    obj.add_copoint("p0", "t1", 50, 30)
    obj.add_copoint("p0", "t2", 40, 40)
    obj.add_copoint("p1", "t1", 70, 10)
    obj.add_copoint("p1", "t3", 50, 90)
    assert obj.copoints["p0"] == ["t1", "t2"]
    assert obj.copoints["p1"] == ["t1", "t3"]
    assert obj.shots["t1"].copoints["p0"] == [50, 30]
    assert obj.shots["t1"].copoints["p1"] == [70, 10]
    assert obj.shots["t2"].copoints["p0"] == [40, 40]
    assert obj.shots["t3"].copoints["p1"] == [50, 90]


def test_add_gcp():
    obj = Worksite(name = "Test")
    obj.add_gcp('"1003"', 13, np.array([1,2,3]))
    assert obj.gcps['"1003"'].name_gcp == '"1003"'
    assert obj.gcps['"1003"'].code == 13
    assert (obj.gcps['"1003"'].coor == np.array([1,2,3])).all()


def test_world_to_image():
    point_terrain = np.array([815601.510, 6283629.280, 54.960])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual = shot.world_to_image(point_terrain, cam, projeucli)
    assert abs(actual[0] - 24042.25) < 7000
    assert abs(actual[1] - 14781.17) < 7000


def test_calculate_coor_img_gcp():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([3,3,3]), np.array([1,1,1]), 'cam_test')
    work.shots['shot_test'].mat_rot = np.array([[1,2,3],
                                           [3,1,2],
                                           [1,1,1]])
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 5, 5, 10)
    work.add_copoint('gcp_test', 'shot_test', 20, 30)
    work.check_cop = True
    work.add_gcp('gcp_test', 3, np.array([1,1,1]))
    work.check_gcp = True
    work.calculate_coor_img_gcp()
    assert round(work.shots['shot_test'].gcps['gcp_test'][0]) == 19
    assert round(work.shots['shot_test'].gcps['gcp_test'][1]) == 23


def test_barycentre():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test')
    work.add_shot("shot2", np.array([3,6,6]), np.array([1,1,1]), 'cam_test')
    work.add_shot("shot3", np.array([2,8,10]), np.array([1,1,1]), 'cam_test')
    work.add_shot("shot4", np.array([2,10,14]), np.array([1,1,1]), 'cam_test')
    bary = work.calculate_barycentre()
    assert bary[0] == 2
    assert bary[1] == 8
    assert bary[2] == 8


def test_image_to_world():
    point_image = np.array([24042.25, 14781.17])
    shot = Shot("test_shot", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    proj = ProjEngine("EPSG:2154", {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084'})
    projeucli = EuclideanProj(814975.925, 6283986.148, proj)
    actual = shot.image_to_world(point_image[0],point_image[1],cam,projeucli)
    assert abs(actual[0] - 815601.510) < 1000
    assert abs(actual[1] - 6283629.280) < 1000
    assert actual[2] == 0
