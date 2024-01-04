"""
Script test function of function files
"""
import numpy as np
from src.functions.tools import func_img
from src.datastruct.shot import Shot
from src.datastruct.camera import Camera


def test_func_img():
    shot = Shot("test", np.array([3,3,3]), np.array([1,1,1]), 'cam_test')
    shot.mat_rot = np.array([[1,2,3],
                             [3,1,2],
                             [1,1,1]])
    cam = Camera('test_cam', 5, 5, 10)
    coor = func_img(np.array([1,1,1]), shot, cam)
    assert (coor == np.array([-15.0, -15.0])).all()
