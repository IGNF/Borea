"""
Script to test function write of rpc.
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument, duplicate-code
import os
import numpy as np
from borea.worksite.worksite import Worksite
from borea.writer.writer_rpc import write


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]
OUTPUT = "./test/tmp"


def setup_module(module):  # run before the first test
    os.makedirs(OUTPUT, exist_ok=True)


def test_write_rpc():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(2154, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot()
    write(None, OUTPUT,
          {"size_grid": 100, "order": 3, "fact_rpc": None, "epsg_output": None}, work)
    assert os.path.exists("./test/tmp/23FD1305x00026_01306_RPC.TXT")
    assert os.path.exists("./test/tmp/23FD1305x00026_01307_RPC.TXT")
    assert os.path.exists("./test/tmp/23FD1305x00026_01308_RPC.TXT")


def test_write_rpc_4326():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(2154, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot()
    write(None, OUTPUT,
          {"size_grid": 100, "order": 3, "fact_rpc": None, "epsg_output": 4326}, work)
    assert os.path.exists("./test/tmp/23FD1305x00026_01306_RPC.TXT")
    assert os.path.exists("./test/tmp/23FD1305x00026_01307_RPC.TXT")
    assert os.path.exists("./test/tmp/23FD1305x00026_01308_RPC.TXT")
