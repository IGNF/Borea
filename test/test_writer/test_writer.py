"""
Script test for module writer
"""
import os
import numpy as np
import shutil as shutil
from src.datastruct.worksite import Worksite
from src.writer.writer_opk import write
from src.reader.orientation.manage_reader import reader_orientation


OUTPUT = "./test/tmp"
FILENAME = "Test"
LINE = [1, None]
HEADER = ['N','X','Y','Zal','Od','Pd','Kd','C']


def setup_module(module): # run before the first test
    try:  # Clean folder test if exists
        shutil.rmtree(OUTPUT)
    except FileNotFoundError:
        pass
    os.makedirs(OUTPUT, exist_ok=True)


def test_writer():
    obj = Worksite(name = FILENAME)
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam", "d")
    write(OUTPUT, obj)
    obj2 = reader_orientation(f"{OUTPUT}/{FILENAME}.opk", LINE, HEADER)
    assert obj2.name == "Test"
    assert obj2.shots["test_shot"].name_shot == "test_shot"
    assert obj2.shots["test_shot"].pos_shot[0] == 1
    assert obj2.shots["test_shot"].pos_shot[1] == 2
    assert obj2.shots["test_shot"].pos_shot[2] == 3
    assert obj2.shots["test_shot"].ori_shot[0] == 3
    assert obj2.shots["test_shot"].ori_shot[1] == 2
    assert obj2.shots["test_shot"].ori_shot[2] == 1
    assert obj2.shots["test_shot"].name_cam == "test_cam"
