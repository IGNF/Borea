"""
Script test for module copoints_pos
"""
import numpy as np
from src.datastruct.worksite import Worksite
from src.transform_world_image.transform_worksite.copoints_pos import copoints_position


def test_copoints_position():
    work = Worksite("Test")