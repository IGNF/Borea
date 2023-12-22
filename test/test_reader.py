"""
Script test to read file
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.orientation.reader_opk import read as read_opk
from src.reader.camera.reader_camera import reader_camera, camera_txt, camera_xml
from src.datastruct.worksite import Worksite


def test_reader_opk():
    obj = read_opk("test/data/Sommets_hEllips_test.opk", None)
    assert obj.name == "Sommets_hEllips_test"
    assert obj.shots[0].name_shot == "22FD2405Ax00001_21104"
    assert obj.shots[0].pos_shot[0] == 546166.732
    assert obj.shots[0].pos_shot[1] == 6504508.606
    assert obj.shots[0].pos_shot[2] == 2081.626
    assert obj.shots[0].ori_shot[0] == -0.2015
    assert obj.shots[0].ori_shot[1] == -0.1173
    assert obj.shots[0].ori_shot[2] == 61.0088
    assert obj.shots[0].name_cam == "UCE-M3-f120-s06"
    assert obj.shots[-1].name_shot == "22FD2405Ax00002_21121"
    assert obj.shots[-1].pos_shot[0] == 547789.766
    assert obj.shots[-1].pos_shot[1] == 6503011.873
    assert obj.shots[-1].pos_shot[2] == 2080.564
    assert obj.shots[-1].ori_shot[0] == 0.1471
    assert obj.shots[-1].ori_shot[1] == 0.0971
    assert obj.shots[-1].ori_shot[2] == -118.1551
    assert obj.shots[-1].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 8


def test_reader_file():
    obj = reader_orientation("test/data/Sommets_hEllips_test.opk")
    assert obj.name == "Sommets_hEllips_test"
    assert obj.shots[0].name_shot == "22FD2405Ax00001_21104"
    assert obj.shots[0].pos_shot[0] == 546166.732
    assert obj.shots[0].pos_shot[1] == 6504508.606
    assert obj.shots[0].pos_shot[2] == 2081.626
    assert obj.shots[0].ori_shot[0] == -0.2015
    assert obj.shots[0].ori_shot[1] == -0.1173
    assert obj.shots[0].ori_shot[2] == 61.0088
    assert obj.shots[0].name_cam == "UCE-M3-f120-s06"
    assert obj.shots[-1].name_shot == "22FD2405Ax00002_21121"
    assert obj.shots[-1].pos_shot[0] == 547789.766
    assert obj.shots[-1].pos_shot[1] == 6503011.873
    assert obj.shots[-1].pos_shot[2] == 2080.564
    assert obj.shots[-1].ori_shot[0] == 0.1471
    assert obj.shots[-1].ori_shot[1] == 0.0971
    assert obj.shots[-1].ori_shot[2] == -118.1551
    assert obj.shots[-1].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 8


def test_read_camera_xml():
    work = Worksite("Test")
    camera_xml("test/data/s07_UC_Eagle_M3_120.xml", work)
    assert work.cameras[0].name_camera == "UCE-M3-f120-s07"
    assert work.cameras[0].ppax == 13230.00
    assert work.cameras[0].ppay == 8502.00
    assert work.cameras[0].focal == 30975.00


def test_read_camera_txt():
    work = Worksite("Test")
    camera_txt("test/data/Camera.txt", work)
    assert work.cameras[0].name_camera == "UCE-M3-f120-s06"
    assert work.cameras[0].ppax == 13210.00
    assert work.cameras[0].ppay == 8502.00
    assert work.cameras[0].focal == 30975.00


def test_read_camera():
    work = Worksite("Test")
    reader_camera(["test/data/s07_UC_Eagle_M3_120.xml", "test/data/Camera.txt"], work)
    assert work.cameras[0].name_camera == "UCE-M3-f120-s07"
    assert work.cameras[0].ppax == 13230.00
    assert work.cameras[0].ppay == 8502.00
    assert work.cameras[0].focal == 30975.00
    assert work.cameras[1].name_camera == "UCE-M3-f120-s06"
    assert work.cameras[1].ppax == 13210.00
    assert work.cameras[1].ppay == 8502.00
    assert work.cameras[1].focal == 30975.00