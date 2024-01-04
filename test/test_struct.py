"""
Script test for function classes
"""
import numpy as np

from src.datastruct.worksite import Worksite
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera
from src.datastruct.gcp import GCP


def test_worksite():
    obj = Worksite(name = "Test")
    assert obj.name == "Test"
    assert obj.shots == {}
    assert obj.cameras == {}


def test_shot():
    obj = Shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    assert obj.name_shot == "test_shot"
    assert obj.pos_shot[0] == 1
    assert obj.pos_shot[1] == 2
    assert obj.pos_shot[2] == 3
    assert obj.ori_shot[0] == 3
    assert obj.ori_shot[1] == 2
    assert obj.ori_shot[2] == 1
    assert obj.name_cam == "test_cam"
    assert obj.copoints == {}


def test_camera():
    obj = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    assert obj.name_camera == "test_cam"
    assert obj.ppax == 13210.00
    assert obj.ppay == 8502.00
    assert obj.focal == 30975.00


def test_addshot():
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


def test_addcam():
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


def test_gcp():
    obj = GCP('"1003"', 3, np.array([1,2,3]))
    assert obj.name_gcp == '"1003"'
    assert obj.code == 3
    assert (obj.coor == np.array([1,2,3])).all()


def test_add_gcp():
    obj = Worksite(name = "Test")
    obj.add_gcp('"1003"', 13, np.array([1,2,3]))
    assert obj.gcps['"1003"'].name_gcp == '"1003"'
    assert obj.gcps['"1003"'].code == 13
    assert (obj.gcps['"1003"'].coor == np.array([1,2,3])).all()


def test_calculate_coor_img_gcp():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([3,3,3]), np.array([1,1,1]), 'cam_test')
    work.shots['shot_test'].mat_rot = np.array([[1,2,3],
                                           [3,1,2],
                                           [1,1,1]])
    work.add_camera('cam_test', 5, 5, 10)
    work.add_copoint('gcp_test', 'shot_test', 20, 30)
    work.check_cop = True
    work.add_gcp('gcp_test', 3, np.array([1,1,1]))
    work.check_gcp = True
    work.calculate_coor_img_gcp()
    assert (work.shots['shot_test'].gcps['gcp_test'] == np.array([-15.0,-15.0])).all()
    