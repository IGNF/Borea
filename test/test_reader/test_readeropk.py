"""
Script test for module reader_opk
"""
# pylint: disable=import-error, missing-function-docstring
import platform
import pytest
from borea.worksite.worksite import Worksite
from borea.reader.orientation.reader_opk import read as read_opk


INPUT_OPK_UBU = "./dataset/23FD1305_alt_test.OPK"
INPUT_OPK_WIN = ".\\dataset\\23FD1305_alt_test.OPK"
UNIT_ANGLE = "degree"


def test_reader_opk_ubupath():
    work = Worksite("23FD1305_alt_test")
    obj = read_opk(INPUT_OPK_UBU, {"order_axe": 'opk', "interval": [2, None],
                                   "header": list("NXYZOPKC"), "unit_angle": UNIT_ANGLE,
                                   "linear_alteration": True}, work)
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
    if platform.system() in ['Linux', 'Darwin']:
        with pytest.raises(FileNotFoundError):
            read_opk(INPUT_OPK_WIN, {"order_axe": 'opk', "interval": [2, None],
                                     "header": list("NXYZOPKC"), "unit_angle": UNIT_ANGLE,
                                     "linear_alteration": True}, work)
    else:
        obj = read_opk(INPUT_OPK_WIN, {"order_axe": 'opk', "interval": [2, None],
                                       "header": list("NXYZOPKC"), "unit_angle": UNIT_ANGLE,
                                       "linear_alteration": True}, work)
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
    with pytest.raises(ValueError):
        read_opk(INPUT_OPK_UBU, {"order_axe": 'opk', "interval": [2, None],
                                 "header": list("NXYZOPKCS"), "unit_angle": UNIT_ANGLE,
                                 "linear_alteration": True}, work)


def test_reader_opk_bad_header_miss_column():
    work = Worksite("23FD1305_alt_test")
    with pytest.raises(ValueError):
        read_opk(INPUT_OPK_UBU, {"order_axe": 'opk', "interval": [2, None],
                                 "header": list("NXYZOPK"), "unit_angle": UNIT_ANGLE,
                                 "linear_alteration": True}, work)


def test_reader_opk_diffheader():
    work = Worksite("23FD1305_alt_test")
    obj = read_opk("test/data/dataset1/23FD1305_alt_NCPOKXYZ.OPK",
                   {"order_axe": 'opk', "interval": [2, None], "header": list("SNCPOKXYZ"),
                    "unit_angle": UNIT_ANGLE, "linear_alteration": True}, work)
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
