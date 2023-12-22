"""
Script test to read file
"""
from src.reader.manage_reader import reader_orientation
from src.reader.reader_opk import read as read_opk


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
