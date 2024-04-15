"""
Test the module conical.py
"""
import os
import pytest
from pathlib import Path, PureWindowsPath
import numpy as np
from src.format.conical import Conical
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera


def setup_module(module): # run before the first test
    os.makedirs("./test/tmp", exist_ok=True)


def test_save_conical():
    shot = Shot("test_shot", np.array([814975.925,6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True, "opk")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004, 4e-6)
    Conical(shot, cam, "LAMBERT93").save_conical(Path(PureWindowsPath("./test/tmp/test_shot.CON")))
    assert os.path.exists("./test/tmp/test_shot.CON")


def test_save_conical_withoutpxsize():
    shot = Shot("test_shot", np.array([814975.925,6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), "test_cam", 'degree',True, "opk")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
    with pytest.raises(ValueError):
        Conical(shot, cam, "LAMBERT93").save_conical(Path(PureWindowsPath("./test/tmp/test_shot.CON")))
