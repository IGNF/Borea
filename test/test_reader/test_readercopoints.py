"""
Script test for module reader_co_points
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_co_points import read_co_points

INPUT_OPK = "./dataset/23FD1305_alt_test.OPK"
INPUT_LIAISONS = "dataset\\liaisons_test.mes"
ARGS = {"interval": [2, None],
        "header": "N X Y Z O P K C",
        "unit_angle": "degree",
        "linear_alteration":True}

def test_read_co_points():
    work = reader_orientation(INPUT_OPK, ARGS)
    read_co_points(INPUT_LIAISONS, work)
    assert work.co_points["MES_674214"] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.co_points["MES_674219"] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.co_points["MES_264193"] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
    assert work.shots["23FD1305x00026_01306"].co_points["MES_674214"] == [3885.75, 14969.14]
    assert work.shots["23FD1305x00026_01306"].co_points["MES_674219"] == [3896.99, 13858.47]
    assert work.shots["23FD1305x00026_01306"].co_points["MES_674216"] == [6033.01, 16208.41]
    assert work.shots["23FD1305x00054_05680"].co_points["MES_145568"] == [559.85, 7656.41]
    assert work.shots["23FD1305x00054_05680"].co_points["MES_145570"] == [436.4, 6604.65]
    assert work.shots["23FD1305x00062_07727"].co_points["MES_264192"] == [4009.15, 5334.46]
    assert work.shots["23FD1305x00062_07727"].co_points["MES_264193"] == [1956.18, 5550.03]
