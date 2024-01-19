"""
Script test for module writer
"""
import os
import numpy as np
import shutil as shutil

from src.datastruct.worksite import Worksite
from src.writer.writer_opk import write
from src.reader.orientation.reader_opk import read as read_opk


OUTPUT = "./test/tmp"
FILENAME = "Test"


def setup_module(): # run before the first test
    os.makedirs(OUTPUT, exist_ok=True)

   
def teardown_module():  # run after the last test
    try:  # Clean folder test if exists
        shutil.rmtree(OUTPUT)
    except FileNotFoundError:
        pass


def test_writer():
    setup_module()
    obj = Worksite(name = FILENAME)
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    write(OUTPUT, obj)
    obj2 = read_opk(os.path.join(OUTPUT,f"{FILENAME}.opk"), 1)
    assert obj2.name == "Test"
    assert obj2.shots["test_shot"].name_shot == "test_shot"
    assert obj2.shots["test_shot"].pos_shot[0] == 1
    assert obj2.shots["test_shot"].pos_shot[1] == 2
    assert obj2.shots["test_shot"].pos_shot[2] == 3
    assert obj2.shots["test_shot"].ori_shot[0] == 3
    assert obj2.shots["test_shot"].ori_shot[1] == 2
    assert obj2.shots["test_shot"].ori_shot[2] == 1
    assert obj2.shots["test_shot"].name_cam == "test_cam"
    teardown_module()