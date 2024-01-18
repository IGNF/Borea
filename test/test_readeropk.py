"""
Script test for module reader_opk
"""
import numpy as np
from src.reader.orientation.reader_opk import read as read_opk

INPUT_OPK = "test/data/23FD1305_alt_test.OPK"

def test_reader_opk():
    obj = read_opk(INPUT_OPK, 1)
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
