"""
Script test for module reader_gcp
"""
import numpy as np
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_gcp import read_gcp

INPUT_OPK = "./test/data/23FD1305_alt_test.OPK"
INPUT_GCP = "./test/data/GCP_test.app"

def test_read_gcp():
    work_gcp = reader_orientation(INPUT_OPK, 1)
    read_gcp([INPUT_GCP], work_gcp)
    assert list(work_gcp.gcps) == ['"1003"','"1005"','"1006"']
    assert work_gcp.gcps['"1003"'].name_gcp == '"1003"'
    assert work_gcp.gcps['"1003"'].code == 13
    assert (work_gcp.gcps['"1003"'].coor == np.array([815601.510, 6283629.280, 54.960])).all()
    assert work_gcp.gcps['"1005"'].name_gcp == '"1005"'
    assert work_gcp.gcps['"1005"'].code == 3
    assert (work_gcp.gcps['"1005"'].coor == np.array([833670.940, 6281965.400, 52.630])).all()
    assert work_gcp.gcps['"1006"'].name_gcp == '"1006"'
    assert work_gcp.gcps['"1006"'].code == 13
    assert (work_gcp.gcps['"1006"'].coor == np.array([838561.350, 6284600.330, 62.470])).all()
