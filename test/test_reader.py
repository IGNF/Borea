"""
Script test to read file
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.orientation.reader_opk import read as read_opk
from src.reader.reader_camera import read_camera, camera_txt, camera_xml
from src.reader.reader_copoints import read_copoints
from src.datastruct.worksite import Worksite

INPUT_OPK = "test/data/23FD1305_alt_test.OPK"
INPUT_CAM_TXT = "test/data/Camera.txt"
INPUT_CAM_XML = "test/data/s07_UC_Eagle_M3_120.xml"
INPUT_LIAISONS = "test/data/liaisons_test.mes"
INPUT_TERRAIN = "test/data/terrain_test.mes"
INPUT_GCP = "test/data/GCP_test.opk"

def test_reader_opk():
    obj = read_opk(INPUT_OPK, None)
    assert obj.name == "23FD1305_alt_test"
    assert obj.shots["23FD1305x00026_01306"].name_shot == "23FD1305x00026_01306"
    assert obj.shots["23FD1305x00026_01306"].pos_shot[0] == 814975.925
    assert obj.shots["23FD1305x00026_01306"].pos_shot[1] == 6283986.148
    assert obj.shots["23FD1305x00026_01306"].pos_shot[2] == 1771.280
    assert obj.shots["23FD1305x00026_01306"].ori_shot[0] == -0.245070686036
    assert obj.shots["23FD1305x00026_01306"].ori_shot[1] == -0.069409621323
    assert obj.shots["23FD1305x00026_01306"].ori_shot[2] == 0.836320989726
    assert obj.shots["23FD1305x00026_01306"].name_cam == "UCE-M3-f120-s06"
    assert obj.shots["23FD1305x00062_07728"].name_shot == "23FD1305x00062_07728"
    assert obj.shots["23FD1305x00062_07728"].pos_shot[0] == 838160.083
    assert obj.shots["23FD1305x00062_07728"].pos_shot[1] == 6284788.913
    assert obj.shots["23FD1305x00062_07728"].pos_shot[2] == 1766.066
    assert obj.shots["23FD1305x00062_07728"].ori_shot[0] == -0.179920958782
    assert obj.shots["23FD1305x00062_07728"].ori_shot[1] == 0.099806773228
    assert obj.shots["23FD1305x00062_07728"].ori_shot[2] == 0.453083308756
    assert obj.shots["23FD1305x00062_07728"].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 7


def test_reader_file():
    obj = reader_orientation(INPUT_OPK)
    assert obj.name == "23FD1305_alt_test"
    assert obj.shots["23FD1305x00026_01306"].name_shot == "23FD1305x00026_01306"
    assert obj.shots["23FD1305x00026_01306"].pos_shot[0] == 814975.925
    assert obj.shots["23FD1305x00026_01306"].pos_shot[1] == 6283986.148
    assert obj.shots["23FD1305x00026_01306"].pos_shot[2] == 1771.280
    assert obj.shots["23FD1305x00026_01306"].ori_shot[0] == -0.245070686036
    assert obj.shots["23FD1305x00026_01306"].ori_shot[1] == -0.069409621323
    assert obj.shots["23FD1305x00026_01306"].ori_shot[2] == 0.836320989726
    assert obj.shots["23FD1305x00026_01306"].name_cam == "UCE-M3-f120-s06"
    assert obj.shots["23FD1305x00062_07728"].name_shot == "23FD1305x00062_07728"
    assert obj.shots["23FD1305x00062_07728"].pos_shot[0] == 838160.083
    assert obj.shots["23FD1305x00062_07728"].pos_shot[1] == 6284788.913
    assert obj.shots["23FD1305x00062_07728"].pos_shot[2] == 1766.066
    assert obj.shots["23FD1305x00062_07728"].ori_shot[0] == -0.179920958782
    assert obj.shots["23FD1305x00062_07728"].ori_shot[1] == 0.099806773228
    assert obj.shots["23FD1305x00062_07728"].ori_shot[2] == 0.453083308756
    assert obj.shots["23FD1305x00062_07728"].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 7


def test_read_camera_xml():
    work = Worksite("Test")
    camera_xml(INPUT_CAM_XML, work)
    assert work.cameras["UCE-M3-f120-s07"].name_camera == "UCE-M3-f120-s07"
    assert work.cameras["UCE-M3-f120-s07"].ppax == 13230.00
    assert work.cameras["UCE-M3-f120-s07"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s07"].focal == 30975.00


def test_read_camera_txt():
    work = Worksite("Test")
    camera_txt(INPUT_CAM_TXT, work)
    assert work.cameras["UCE-M3-f120-s06"].name_camera == "UCE-M3-f120-s06"
    assert work.cameras["UCE-M3-f120-s06"].ppax == 13210.00
    assert work.cameras["UCE-M3-f120-s06"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s06"].focal == 30975.00


def test_read_camera():
    work = Worksite("Test")
    read_camera([INPUT_CAM_XML, INPUT_CAM_TXT], work)
    assert work.cameras["UCE-M3-f120-s07"].name_camera == "UCE-M3-f120-s07"
    assert work.cameras["UCE-M3-f120-s07"].ppax == 13230.00
    assert work.cameras["UCE-M3-f120-s07"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s07"].focal == 30975.00
    assert work.cameras["UCE-M3-f120-s06"].name_camera == "UCE-M3-f120-s06"
    assert work.cameras["UCE-M3-f120-s06"].ppax == 13210.00
    assert work.cameras["UCE-M3-f120-s06"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s06"].focal == 30975.00


def test_read_copoints():
    work = reader_orientation(INPUT_OPK)
    read_copoints([INPUT_LIAISONS], work)
    assert work.copoints["MES_674214"] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.copoints["MES_674219"] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.copoints["MES_264193"] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
    assert work.shots["23FD1305x00026_01306"].copoints["MES_674214"] == [3885.75, 14969.14]
    assert work.shots["23FD1305x00026_01306"].copoints["MES_674219"] == [3896.99, 13858.47]
    assert work.shots["23FD1305x00026_01306"].copoints["MES_674216"] == [6033.01, 16208.41]
    assert work.shots["23FD1305x00054_05680"].copoints["MES_145568"] == [559.85, 7656.41]
    assert work.shots["23FD1305x00054_05680"].copoints["MES_145570"] == [436.4, 6604.65]
    assert work.shots["23FD1305x00062_07727"].copoints["MES_264192"] == [4009.15, 5334.46]
    assert work.shots["23FD1305x00062_07727"].copoints["MES_264193"] == [1956.18, 5550.03]
