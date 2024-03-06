"""
Script test for module worksite
"""
import numpy as np
from src.worksite.worksite import Worksite

PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def test_barycentre():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_shot("shot2", np.array([3,6,6]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_shot("shot3", np.array([2,8,10]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_shot("shot4", np.array([2,10,14]), np.array([1,1,1]), 'cam_test',"degree",True)
    bary = work.calculate_barycentre()
    assert bary[0] == 2
    assert bary[1] == 8
    assert bary[2] == 8


def test_get_numpy():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_co_point("la", "shot1", 10, 10)
    work.add_co_point("do", "shot1", 50, 14)
    work.co_pts_world["la"] = np.array([20, 30, 50])
    work.co_pts_world["do"] = np.array([40, 35, 19])
    img, world = work.get_points_shot_numpy("shot1", "co_points")
    assert (img == np.array([[10, 50], [10, 14]])).all()
    assert (world == np.array([[20, 40], [30, 35], [50, 19]])).all()
