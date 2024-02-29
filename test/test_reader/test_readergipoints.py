"""
Script test for module reader_ground_img_pts
"""
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_ground_img_pts import read_ground_image_points

INPUT_OPK = "./dataset/23FD1305_alt_test.OPK"
INPUT_TERRAIN = "./dataset/terrain_test.mes"
ARGS = {"interval": [2, None],
        "header": "N X Y Z O P K C",
        "unit_angle": "degree",
        "linear_alteration":True}

def test_read_ground_img_pts():
    work = reader_orientation(INPUT_OPK, ARGS)
    read_ground_image_points([INPUT_TERRAIN], work)
    assert work.ground_img_pts['"1003"'] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
    assert work.ground_img_pts['"1005"'] == ["23FD1305x00054_05680", "23FD1305x00054_05681"]
    assert work.ground_img_pts['"1006"'] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
    assert work.shots["23FD1305x00026_01306"].ground_img_pts['"1003"'] == [24042.25, 14781.17]
    assert work.shots["23FD1305x00026_01307"].ground_img_pts['"1003"'] == [24120.2, 10329.3]
    assert work.shots["23FD1305x00026_01308"].ground_img_pts['"1003"'] == [24161.49, 5929.37]
    assert work.shots["23FD1305x00054_05680"].ground_img_pts['"1005"'] == [22796.05, 14371.27]
    assert work.shots["23FD1305x00054_05681"].ground_img_pts['"1005"'] == [22817.4, 9930.73]
    assert work.shots["23FD1305x00062_07727"].ground_img_pts['"1006"'] == [20209.92, 16200.26]
    assert work.shots["23FD1305x00062_07728"].ground_img_pts['"1006"'] == [20329.12, 11794.01]
