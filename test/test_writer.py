import os
import numpy as np
import shutil as shutil

from src.datastruct.worksite import Worksite
from src.writer.writer_opk import write
from src.reader.reader_opk import read as read_opk


def setup_module(module): # run before the first test
    try:  # Clean folder test if exists
        shutil.rmtree("test/tmp")
        os.mkdir("test/tmp")
    except FileNotFoundError:
        pass

     
def teardown_module(module):  # run after the last test
    try:  # Clean folder test if exists
        shutil.rmtree("test/tmp")
        os.mkdir("test/tmp")
    except FileNotFoundError:
        pass


def test_writer():
    obj = Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    write("test/tmp/", obj)
    obj2 = read_opk("test/tmp/Test.opk", None)
    assert obj2.name == "Test"
    assert obj2.shots[0].name_shot == "test_shot"
    assert obj2.shots[0].pos_shot[0] == 1
    assert obj2.shots[0].pos_shot[1] == 2
    assert obj2.shots[0].pos_shot[2] == 3
    assert obj2.shots[0].ori_shot[0] == 3
    assert obj2.shots[0].ori_shot[1] == 2
    assert obj2.shots[0].ori_shot[2] == 1
    assert obj2.shots[0].name_cam == "test_cam"
