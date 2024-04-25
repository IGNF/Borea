"""
Script test for module writer
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
import os
import numpy as np
from src.worksite.worksite import Worksite
from src.writer.writer_con import write


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]
OUTPUT = "./test/tmp"


def setup_module(module):  # run before the first test
    os.makedirs(OUTPUT, exist_ok=True)


def test_write_con():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "UCE-M3-f120-s06", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "UCE-M3-f120-s06", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01308", np.array([814978.586, 6283482.827, 1771.799]),
                  np.array([-0.181570631296,  0.001583051432, 0.493526899473]),
                  "UCE-M3-f120-s06", "degree", True, "opk")
    work.set_proj(2154, PATH_GEOID)
    work.add_camera('UCE-M3-f120-s06', 13210.00, 8502.00, 30975.00, 26460, 17004, 4e-6)
    write(None, OUTPUT, None, work)
    assert os.path.exists("./test/tmp/23FD1305x00026_01306.CON")
    assert os.path.exists("./test/tmp/23FD1305x00026_01307.CON")
    assert os.path.exists("./test/tmp/23FD1305x00026_01308.CON")
