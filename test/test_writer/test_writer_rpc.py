"""
Script to test function write of rpc.
"""
import os
import numpy as np
from src.worksite.worksite import Worksite
from src.writer.writer_rpc import write


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def test_write_rpc():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    write("","./test/tmp/", {"size_grid":100, "order":3, "fact_rpc":1e-6}, work)
    assert os.path.exists("./test/tmp/23FD1305x00026_01306_RPC.txt")
    assert os.path.exists("./test/tmp/23FD1305x00026_01307_RPC.txt")
    assert os.path.exists("./test/tmp/23FD1305x00026_01308_RPC.txt")


def test_write_rpc_name():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test","degree",True)
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot(approx=False)
    write("test","./test/tmp/", {"size_grid":100, "order":3, "fact_rpc":1e-6}, work)
    assert os.path.exists("./test/tmp/test_23FD1305x00026_01306_RPC.txt")
    assert os.path.exists("./test/tmp/test_23FD1305x00026_01307_RPC.txt")
    assert os.path.exists("./test/tmp/test_23FD1305x00026_01308_RPC.txt")
