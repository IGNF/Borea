"""
Script test for module reader_gcp2d
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_gcp2d import read_gcp2d

INPUT_OPK = "./dataset/23FD1305_alt_test.OPK"
INPUT_TERRAIN = "./dataset/terrain_test.mes"
ARGS = {"interval": [2, None],
        "header": "N X Y Z O P K C",
        "unit_angle": "degree",
        "linear_alteration":True}

def test_read_gcp2d():
    work = reader_orientation(INPUT_OPK, ARGS)
    read_gcp2d(INPUT_TERRAIN, work)
    assert work.gcp2d['"1003"'] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.gcp2d['"1005"'] == ["23FD1305x00054_05680", "23FD1305x00054_05681"]
    assert work.gcp2d['"1006"'] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
    assert work.shots["23FD1305x00026_01306"].gcp2d['"1003"'] == [24042.25, 14781.17]
    assert work.shots["23FD1305x00026_01307"].gcp2d['"1003"'] == [24120.2, 10329.3]
    assert work.shots["23FD1305x00026_01308"].gcp2d['"1003"'] == [24161.49, 5929.37]
    assert work.shots["23FD1305x00054_05680"].gcp2d['"1005"'] == [22796.05, 14371.27]
    assert work.shots["23FD1305x00054_05681"].gcp2d['"1005"'] == [22817.4, 9930.73]
    assert work.shots["23FD1305x00062_07727"].gcp2d['"1006"'] == [20209.92, 16200.26]
    assert work.shots["23FD1305x00062_07728"].gcp2d['"1006"'] == [20329.12, 11794.01]
