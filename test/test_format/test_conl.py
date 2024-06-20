"""
Test the module conl.py
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
import os
from pathlib import Path, PureWindowsPath
import numpy as np
from borea.format.conl import Conl
from borea.datastruct.shot import Shot
from borea.datastruct.camera import Camera


def setup_module(module):  # run before the first test
    os.makedirs("./test/tmp", exist_ok=True)


def test_save_conl():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
                np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                "test_cam", 'degree', True, "opk")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
    Conl(shot, cam, "LAMBERT93").save_conl(Path(PureWindowsPath("./test/tmp/test_shot.CON")))
    assert os.path.exists("./test/tmp/test_shot.CON")
