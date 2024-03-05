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
