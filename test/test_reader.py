"""
Script test to read file
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.orientation.reader_opk import read as read_opk
from src.reader.reader_camera import read_camera, camera_txt, camera_xml
from src.reader.reader_copoints import read_copoints
from src.datastruct.worksite import Worksite


def test_reader_opk():
    obj = read_opk("test/data/23FD1305_alt_test.opk", None)
    assert obj.name == "23FD1305_alt_test"
    assert obj.shots["23FD1305x00001_00003"].name_shot == "23FD1305x00001_00003"
    assert obj.shots["23FD1305x00001_00003"].pos_shot[0] == 798744.352
    assert obj.shots["23FD1305x00001_00003"].pos_shot[1] == 6262815.867
    assert obj.shots["23FD1305x00001_00003"].pos_shot[2] == 1778.451
    assert obj.shots["23FD1305x00001_00003"].ori_shot[0] == 0.157339710405
    assert obj.shots["23FD1305x00001_00003"].ori_shot[1] == 0.010129647126
    assert obj.shots["23FD1305x00001_00003"].ori_shot[2] == -179.310680057325
    assert obj.shots["23FD1305x00001_00003"].name_cam == "UCE-M3-f120-s06"
    assert obj.shots["23FD1305x00002_00053"].name_shot == "23FD1305x00002_00053"
    assert obj.shots["23FD1305x00002_00053"].pos_shot[0] == 799387.667
    assert obj.shots["23FD1305x00002_00053"].pos_shot[1] == 6263051.508
    assert obj.shots["23FD1305x00002_00053"].pos_shot[2] == 1784.760
    assert obj.shots["23FD1305x00002_00053"].ori_shot[0] == -0.146630494647
    assert obj.shots["23FD1305x00002_00053"].ori_shot[1] == -0.031919390293
    assert obj.shots["23FD1305x00002_00053"].ori_shot[2] == -0.209336104979
    assert obj.shots["23FD1305x00002_00053"].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 7


def test_reader_file():
    obj = reader_orientation("test/data/23FD1305_alt_test.opk")
    assert obj.name == "23FD1305_alt_test"
    assert obj.shots["23FD1305x00001_00003"].name_shot == "23FD1305x00001_00003"
    assert obj.shots["23FD1305x00001_00003"].pos_shot[0] == 798744.352
    assert obj.shots["23FD1305x00001_00003"].pos_shot[1] == 6262815.867
    assert obj.shots["23FD1305x00001_00003"].pos_shot[2] == 1778.451
    assert obj.shots["23FD1305x00001_00003"].ori_shot[0] == 0.157339710405
    assert obj.shots["23FD1305x00001_00003"].ori_shot[1] == 0.010129647126
    assert obj.shots["23FD1305x00001_00003"].ori_shot[2] == -179.310680057325
    assert obj.shots["23FD1305x00001_00003"].name_cam == "UCE-M3-f120-s06"
    assert obj.shots["23FD1305x00002_00053"].name_shot == "23FD1305x00002_00053"
    assert obj.shots["23FD1305x00002_00053"].pos_shot[0] == 799387.667
    assert obj.shots["23FD1305x00002_00053"].pos_shot[1] == 6263051.508
    assert obj.shots["23FD1305x00002_00053"].pos_shot[2] == 1784.760
    assert obj.shots["23FD1305x00002_00053"].ori_shot[0] == -0.146630494647
    assert obj.shots["23FD1305x00002_00053"].ori_shot[1] == -0.031919390293
    assert obj.shots["23FD1305x00002_00053"].ori_shot[2] == -0.209336104979
    assert obj.shots["23FD1305x00002_00053"].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 7


def test_read_camera_xml():
    work = Worksite("Test")
    camera_xml("test/data/s07_UC_Eagle_M3_120.xml", work)
    assert work.cameras["UCE-M3-f120-s07"].name_camera == "UCE-M3-f120-s07"
    assert work.cameras["UCE-M3-f120-s07"].ppax == 13230.00
    assert work.cameras["UCE-M3-f120-s07"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s07"].focal == 30975.00


def test_read_camera_txt():
    work = Worksite("Test")
    camera_txt("test/data/Camera.txt", work)
    assert work.cameras["UCE-M3-f120-s06"].name_camera == "UCE-M3-f120-s06"
    assert work.cameras["UCE-M3-f120-s06"].ppax == 13210.00
    assert work.cameras["UCE-M3-f120-s06"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s06"].focal == 30975.00


def test_read_camera():
    work = Worksite("Test")
    read_camera(["test/data/s07_UC_Eagle_M3_120.xml", "test/data/Camera.txt"], work)
    assert work.cameras["UCE-M3-f120-s07"].name_camera == "UCE-M3-f120-s07"
    assert work.cameras["UCE-M3-f120-s07"].ppax == 13230.00
    assert work.cameras["UCE-M3-f120-s07"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s07"].focal == 30975.00
    assert work.cameras["UCE-M3-f120-s06"].name_camera == "UCE-M3-f120-s06"
    assert work.cameras["UCE-M3-f120-s06"].ppax == 13210.00
    assert work.cameras["UCE-M3-f120-s06"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s06"].focal == 30975.00


def test_read_copoints():
    work = reader_orientation("test/data/23FD1305_alt_test.opk")
    read_copoints(["test/data/all_liaisons.mes"], work)
    assert work.copoints["MES_0"] == ["23FD1305x00001_00003", "23FD1305x00001_00004"]
    assert work.copoints["MES_1"] == ["23FD1305x00001_00003", "23FD1305x00001_00004", "23FD1305x00001_00005", "23FD1305x00001_00006", "23FD1305x00002_00051", "23FD1305x00002_00052", "23FD1305x00002_00053"]
    assert work.copoints["MES_2"] == ["23FD1305x00001_00003", "23FD1305x00001_00005", "23FD1305x00001_00006", "23FD1305x00002_00051", "23FD1305x00002_00052", "23FD1305x00002_00053"]
    assert work.shots["23FD1305x00001_00003"].copoints["MES_0"] == [4763.57, 16960.5]
    assert work.shots["23FD1305x00001_00003"].copoints["MES_1"] == [6818.89, 16625.93]
    assert work.shots["23FD1305x00001_00003"].copoints["MES_2"] == [6165.08, 16873.72]
    assert work.shots["23FD1305x00001_00004"].copoints["MES_0"] == [4813.98, 12509.25]
    assert work.shots["23FD1305x00001_00004"].copoints["MES_1"] == [6869.3, 12187.65]
    assert work.shots["23FD1305x00002_00053"].copoints["MES_1"] == [8270.79, 4265.72]
    assert work.shots["23FD1305x00002_00053"].copoints["MES_2"] == [8908.58, 4012.49]
