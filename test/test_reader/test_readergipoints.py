"""
Script test for module reader_gipoints
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_gipoints import read_gipoints

INPUT_OPK = "./test/data/23FD1305_alt_test.OPK"
INPUT_TERRAIN = "./test/data/terrain_test.mes"
LINE = [1, None]
HEADER = ['N','X','Y','Zal','Od','Pd','Kd','C']

def test_read_gipoints():
    work = reader_orientation(INPUT_OPK, LINE, HEADER)
    read_gipoints([INPUT_TERRAIN], work)
    assert work.gipoints['"1003"'] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.gipoints['"1005"'] == ["23FD1305x00054_05680", "23FD1305x00054_05681"]
    assert work.gipoints['"1006"'] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
    assert work.shots["23FD1305x00026_01306"].gipoints['"1003"'] == [24042.25, 14781.17]
    assert work.shots["23FD1305x00026_01307"].gipoints['"1003"'] == [24120.2, 10329.3]
    assert work.shots["23FD1305x00026_01308"].gipoints['"1003"'] == [24161.49, 5929.37]
    assert work.shots["23FD1305x00054_05680"].gipoints['"1005"'] == [22796.05, 14371.27]
    assert work.shots["23FD1305x00054_05681"].gipoints['"1005"'] == [22817.4, 9930.73]
    assert work.shots["23FD1305x00062_07727"].gipoints['"1006"'] == [20209.92, 16200.26]
    assert work.shots["23FD1305x00062_07728"].gipoints['"1006"'] == [20329.12, 11794.01]
