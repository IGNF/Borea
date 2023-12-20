import os
import numpy as np
import shutil as shutil
import code.worksite as ws
import code.reader as r
import code.writer as w


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


def test_worksite():
    obj = ws.Worksite(name = "Test")
    assert obj.name == "Test"
    assert obj.shots == []


def test_addshot():
    obj = ws.Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    assert obj.shots[0].name_shot == "test_shot"
    assert obj.shots[0].pos_shot[0] == 1
    assert obj.shots[0].pos_shot[1] == 2
    assert obj.shots[0].pos_shot[2] == 3
    assert obj.shots[0].ori_shot[0] == 3
    assert obj.shots[0].ori_shot[1] == 2
    assert obj.shots[0].ori_shot[2] == 1
    assert obj.shots[0].name_cam == "test_cam"


def test_reader():
    obj = r.from_opk("test/data/Sommets_hEllips_test.opk")
    assert obj.name == "Sommets_hEllips_test"
    assert obj.shots[0].name_shot == "22FD2405Ax00001_21104"
    assert obj.shots[0].pos_shot[0] == 546166.732
    assert obj.shots[0].pos_shot[1] == 6504508.606
    assert obj.shots[0].pos_shot[2] == 2081.626
    assert obj.shots[0].ori_shot[0] == -0.2015
    assert obj.shots[0].ori_shot[1] == -0.1173
    assert obj.shots[0].ori_shot[2] == 61.0088
    assert obj.shots[0].name_cam == "UCE-M3-f120-s06"
    assert obj.shots[-1].name_shot == "22FD2405Ax00002_21121"
    assert obj.shots[-1].pos_shot[0] == 547789.766
    assert obj.shots[-1].pos_shot[1] == 6503011.873
    assert obj.shots[-1].pos_shot[2] == 2080.564
    assert obj.shots[-1].ori_shot[0] == 0.1471
    assert obj.shots[-1].ori_shot[1] == 0.0971
    assert obj.shots[-1].ori_shot[2] == -118.1551
    assert obj.shots[-1].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 8


def test_writer():
    obj = ws.Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    w.to_opk("test/tmp/", obj)
    obj2 = r.from_opk("test/tmp/Test.opk")
    assert obj2.name == "Test"
    assert obj2.shots[0].name_shot == "test_shot"
    assert obj2.shots[0].pos_shot[0] == 1
    assert obj2.shots[0].pos_shot[1] == 2
    assert obj2.shots[0].pos_shot[2] == 3
    assert obj2.shots[0].ori_shot[0] == 3
    assert obj2.shots[0].ori_shot[1] == 2
    assert obj2.shots[0].ori_shot[2] == 1
    assert obj2.shots[0].name_cam == "test_cam"


def test_reader_file():
    obj = r.from_file("test/data/Sommets_hEllips_test.opk")
    assert obj.name == "Sommets_hEllips_test"
    assert obj.shots[0].name_shot == "22FD2405Ax00001_21104"
    assert obj.shots[0].pos_shot[0] == 546166.732
    assert obj.shots[0].pos_shot[1] == 6504508.606
    assert obj.shots[0].pos_shot[2] == 2081.626
    assert obj.shots[0].ori_shot[0] == -0.2015
    assert obj.shots[0].ori_shot[1] == -0.1173
    assert obj.shots[0].ori_shot[2] == 61.0088
    assert obj.shots[0].name_cam == "UCE-M3-f120-s06"
    assert obj.shots[-1].name_shot == "22FD2405Ax00002_21121"
    assert obj.shots[-1].pos_shot[0] == 547789.766
    assert obj.shots[-1].pos_shot[1] == 6503011.873
    assert obj.shots[-1].pos_shot[2] == 2080.564
    assert obj.shots[-1].ori_shot[0] == 0.1471
    assert obj.shots[-1].ori_shot[1] == 0.0971
    assert obj.shots[-1].ori_shot[2] == -118.1551
    assert obj.shots[-1].name_cam == "UCE-M3-f120-s06"
    assert len(obj.shots) == 8
