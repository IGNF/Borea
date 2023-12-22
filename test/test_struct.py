import numpy as np

from src.datastruct.worksite import Worksite
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera


def test_worksite():
    obj = Worksite(name = "Test")
    assert obj.name == "Test"
    assert obj.shots == []


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


def test_camera():
    obj = Camera("test_cam", 13210.00, 8502.00, 30975.00)
    assert obj.name_camera == "test_cam"
    assert obj.ppax == 13210.00
    assert obj.ppay == 8502.00
    assert obj.focal == 30975.00


def test_addshot():
    obj = Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    assert obj.shots[0].name_shot == "test_shot"
    assert obj.shots[0].pos_shot[0] == 1
    assert obj.shots[0].pos_shot[1] == 2
    assert obj.shots[0].pos_shot[2] == 3
    assert obj.shots[0].ori_shot[0] == 3
    assert obj.shots[0].ori_shot[1] == 2
    assert obj.shots[0].ori_shot[2] == 1
    assert obj.shots[0].name_cam == "test_cam"


def test_addcam():
    obj = Worksite(name = "Test")
    obj.add_camera("test_cam", 13210.00, 8502.00, 30975.00)
    assert obj.cameras[0].name_camera == "test_cam"
    assert obj.cameras[0].ppax== 13210.00
    assert obj.cameras[0].ppay == 8502.00
    assert obj.cameras[0].focal == 30975.00
