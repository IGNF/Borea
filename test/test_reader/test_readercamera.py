"""
Script test for module reader_camera
"""
from src.reader.reader_camera import read_camera, camera_txt, camera_xml
from src.datastruct.worksite import Worksite

INPUT_CAM_TXT = "test/data/Camera.txt"
INPUT_CAM_XML = "test/data/s07_UC_Eagle_M3_120.xml"

def test_read_camera_xml():
    work = Worksite("Test")
    camera_xml(INPUT_CAM_XML, work)
    assert work.cameras["UCE-M3-f120-s07"].name_camera == "UCE-M3-f120-s07"
    assert work.cameras["UCE-M3-f120-s07"].ppax == 13230.00
    assert work.cameras["UCE-M3-f120-s07"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s07"].focal == 30975.00
    assert work.cameras["UCE-M3-f120-s07"].width == 26460.00
    assert work.cameras["UCE-M3-f120-s07"].height == 17004.00


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
