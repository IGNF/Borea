"""
Script test for module reader_opk
"""
import platform
import pytest
from src.datastruct.worksite import Worksite
from src.reader.orientation.reader_opk import read as read_opk

INPUT_OPK_UBU = "./test/data/23FD1305_alt_test.OPK"
INPUT_OPK_WIN = ".\\test\\data\\23FD1305_alt_test.OPK"
LINE = [1, None]
HEADER = ['N','X','Y','Z','O','P','K','C']

def test_reader_opk_ubupath():
    work = Worksite("23FD1305_alt_test")
    obj = read_opk(INPUT_OPK_UBU, LINE, HEADER, work)
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
            obj = read_opk(INPUT_OPK_WIN, LINE, HEADER, work)
    else:
        obj = read_opk(INPUT_OPK_WIN, LINE, HEADER, work)
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
