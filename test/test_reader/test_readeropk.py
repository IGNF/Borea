"""
Script test for module reader_opk
"""
import platform
import pytest
from src.worksite.worksite import Worksite
from src.reader.orientation.reader_opk import read as read_opk

INPUT_OPK_UBU = "./dataset/23FD1305_alt_test.OPK"
INPUT_OPK_WIN = ".\\dataset\\23FD1305_alt_test.OPK"
LINE = [2, None]
UNIT_ANGLE = "degree"
ARGS = {"interval": LINE,
        "header": "N X Y Z O P K C",
        "unit_angle": UNIT_ANGLE,
        "linear_alteration":True}

def test_reader_opk_ubupath():
    work = Worksite("23FD1305_alt_test")
    obj = read_opk(INPUT_OPK_UBU, ARGS, work)
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


def test_reader_opk_winpath():
    work = Worksite("23FD1305_alt_test")
    if platform.system() in ['Linux','Darwin']:
        with pytest.raises(FileNotFoundError) as e_info:
            obj = read_opk(INPUT_OPK_WIN, ARGS, work)
    else:
        obj = read_opk(INPUT_OPK_WIN, ARGS, work)
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


def test_reader_opk_bad_header_add_column():
    work = Worksite("23FD1305_alt_test")
    with pytest.raises(ValueError) as e_info:
        obj = read_opk(INPUT_OPK_UBU, {"interval": LINE,"header": "N X Y Z O P K C S","unit_angle": UNIT_ANGLE,"linear_alteration":True}, work)


def test_reader_opk_bad_header_miss_column():
    work = Worksite("23FD1305_alt_test")
    with pytest.raises(ValueError) as e_info:
        obj = read_opk(INPUT_OPK_UBU, {"interval": LINE,"header": "N X Y Z O P K","unit_angle": UNIT_ANGLE,"linear_alteration":True}, work)


def test_reader_opk_diffheader():
    work = Worksite("23FD1305_alt_test")
    obj = read_opk("test/data/dataset1/23FD1305_alt_NCPOKXYZ.OPK", {"interval": LINE,"header": "S N C P O K X Y Z","unit_angle": UNIT_ANGLE,"linear_alteration":True}, work)
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