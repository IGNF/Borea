"""
Script test for module reader_camera
"""
from src.reader.reader_camera import read_camera, camera_txt
from src.worksite.worksite import Worksite

INPUT_CAM1_TXT = "./dataset/Camera1.txt"
INPUT_CAM2_TXT = ".\\dataset\\Camera2.txt"



def test_read_camera_txt():
    work = Worksite("Test")
    camera_txt(INPUT_CAM1_TXT, work)
    assert work.cameras["UCE-M3-f120-s06"].name_camera == "UCE-M3-f120-s06"
    assert work.cameras["UCE-M3-f120-s06"].ppax == 13210.00
    assert work.cameras["UCE-M3-f120-s06"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s06"].focal == 30975.00
    assert work.cameras["UCE-M3-f120-s06"].width == 26460
    assert work.cameras["UCE-M3-f120-s06"].height == 17004
    assert work.cameras["UCE-M3-f120-s06"].pixel_size == 4e-06


def test_read_camera():
    work = Worksite("Test")
    read_camera([INPUT_CAM1_TXT, INPUT_CAM2_TXT], work)
    assert work.cameras["UCE-M3-f120-s07"].name_camera == "UCE-M3-f120-s07"
    assert work.cameras["UCE-M3-f120-s07"].ppax == 13230.00
    assert work.cameras["UCE-M3-f120-s07"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s07"].focal == 30975.00
    assert work.cameras["UCE-M3-f120-s07"].width == 26460
    assert work.cameras["UCE-M3-f120-s07"].height == 17004
    assert work.cameras["UCE-M3-f120-s06"].name_camera == "UCE-M3-f120-s06"
    assert work.cameras["UCE-M3-f120-s06"].ppax == 13210.00
    assert work.cameras["UCE-M3-f120-s06"].ppay == 8502.00
    assert work.cameras["UCE-M3-f120-s06"].focal == 30975.00
    assert work.cameras["UCE-M3-f120-s06"].width == 26460
    assert work.cameras["UCE-M3-f120-s06"].height == 17004
