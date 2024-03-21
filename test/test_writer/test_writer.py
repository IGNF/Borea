"""
Script test for module writer
"""
import os
import numpy as np
import shutil as shutil
from src.worksite.worksite import Worksite
from src.writer.writer_opk import write
from src.reader.orientation.manage_reader import reader_orientation


OUTPUT = "./test/tmp"
FILENAME = "Test"
ARGS = {"interval": [2, None],
        "header": list("NXYZOPKC"),
        "unit_angle": "radian",
        "linear_alteration":True}
OUTPUT_NAME = "Test_output"
OUTPUT_ARGS = {"header": list("NOPKCXYZ"),
               "unit_angle": "radian",
               "linear_alteration":True}
INPUT_OUTPUT_ARGS = {"interval": [2, None],
                     "header": list("NOPKCXYZ"),
                     "unit_angle": "radian",
                     "linear_alteration":True}


def setup_module(module): # run before the first test
    os.makedirs(OUTPUT, exist_ok=True)


def test_writer():
    obj = Worksite(name = FILENAME)
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([180,0,360]), "test_cam", "degree",True)
    obj.add_camera("test_cam",0,0,0,0,0)
    obj.type_z_shot = "altitude"
    write(OUTPUT_NAME,OUTPUT,OUTPUT_ARGS,obj)
    obj2 = reader_orientation(f"{OUTPUT}/{OUTPUT_NAME}.opk", INPUT_OUTPUT_ARGS)
    assert obj2.name == "Test_output"
    assert obj2.shots["test_shot"].name_shot == "test_shot"
    assert obj2.shots["test_shot"].pos_shot[0] == 1
    assert obj2.shots["test_shot"].pos_shot[1] == 2
    assert obj2.shots["test_shot"].pos_shot[2] == 3
    assert obj2.shots["test_shot"].ori_shot[0] == np.pi
    assert obj2.shots["test_shot"].ori_shot[1] == 0
    assert obj2.shots["test_shot"].ori_shot[2] == 2*np.pi
    assert obj2.shots["test_shot"].name_cam == "test_cam"
