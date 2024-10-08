"""
Script test for module worksite
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument
import numpy as np
import pandas as pd
import pytest
from borea.datastruct.dtm import Dtm
from borea.geodesy.proj_engine import ProjEngine
from borea.worksite.worksite import Worksite


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
EPSGFR = [2154]
EPSGAR = [4339]
LIST_GEOID = ["./dataset/fr_ign_RAF20.tif"]


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_barycentre():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1, 8, 2]), np.array([1, 1, 1]),
                  'cam_test', "degree", True, "opk")
    work.add_shot("shot2", np.array([3, 6, 6]), np.array([1, 1, 1]),
                  'cam_test', "degree", True, "opk")
    work.add_shot("shot3", np.array([2, 8, 10]), np.array([1, 1, 1]),
                  'cam_test', "degree", True, "opk")
    work.add_shot("shot4", np.array([2, 10, 14]), np.array([1, 1, 1]),
                  'cam_test', "degree", True, "opk")
    bary = work.calculate_barycentre()
    assert bary[0] == 2
    assert bary[1] == 8
    assert bary[2] == 8


def test_get_copts_img_world():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1, 8, 2]), np.array([1, 1, 1]),
                  'cam_test', "degree", True, "opk")
    work.add_co_point("la", "shot1", np.array([10, 10]))
    work.add_co_point("do", "shot1", np.array([50, 14]))
    work.co_pts_world["la"] = np.array([20, 30, 50])
    work.co_pts_world["do"] = np.array([40, 35, 19])
    img, world = work.get_coor_pt_img_and_world("shot1", "co_points")
    assert (img == np.array([[10, 50], [10, 14]])).all()
    assert (world == np.array([[20, 40], [30, 35], [50, 19]])).all()


def test_get_gcp_img_world():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1, 8, 2]), np.array([1, 1, 1]),
                  'cam_test', "degree", True, "opk")
    work.add_gcp2d("la", "shot1", np.array([10, 10]))
    work.add_gcp2d("do", "shot1", np.array([50, 14]))
    work.gcp2d_in_world["la"] = np.array([20, 30, 50])
    work.gcp2d_in_world["do"] = np.array([40, 35, 19])
    img, world = work.get_coor_pt_img_and_world("shot1", "gcp2d")
    assert (img == np.array([[10, 50], [10, 14]])).all()
    assert (world == np.array([[20, 40], [30, 35], [50, 19]])).all()


def test_get_point_dataframe_copoints():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_shot("t2", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_shot("t3", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_co_point("p0", "t1", np.array([50, 30]))
    obj.add_co_point("p0", "t2", np.array([40, 40]))
    obj.add_co_point("p1", "t1", np.array([70, 10]))
    obj.add_co_point("p1", "t3", np.array([50, 90]))
    pd_pt = obj.get_point_image_dataframe("co_points", [])
    assert (pd_pt["id_pt"].to_numpy() == np.array(["p0", "p0", "p1", "p1"])).all()
    assert (pd_pt["id_img"].to_numpy() == np.array(["t1", "t2", "t1", "t3"])).all()
    assert (pd_pt["column"].to_numpy() == np.array([50, 40, 70, 50])).all()
    assert (pd_pt["line"].to_numpy() == np.array([30, 40, 10, 90])).all()


def test_get_point_dataframe_groundimgpt():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_shot("t2", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_shot("t3", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_gcp2d("p0", "t1", np.array([50, 30]))
    obj.add_gcp2d("p0", "t2", np.array([40, 40]))
    obj.add_gcp2d("p1", "t1", np.array([70, 10]))
    obj.add_gcp2d("p1", "t3", np.array([50, 90]))
    obj.add_gcp3d('p0', 13, np.array([1, 2, 3]))
    obj.add_gcp3d('p1', 3, np.array([1, 2, 3]))
    pd_pt = obj.get_point_image_dataframe("gcp2d", [13])
    assert (pd_pt["id_pt"].to_numpy() == np.array(["p0", "p0"])).all()
    assert (pd_pt["id_img"].to_numpy() == np.array(["t1", "t2"])).all()
    assert (pd_pt["column"].to_numpy() == np.array([50, 40])).all()
    assert (pd_pt["line"].to_numpy() == np.array([30, 40])).all()


def test_set_point_dataframe():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_shot("t2", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_shot("t3", np.array([1, 2, 3]), np.array([3, 2, 1]),
                 "test_cam", "degree", True, "opk")
    obj.add_co_point("p0", "t1", np.array([50, 30]))
    obj.add_co_point("p0", "t2", np.array([40, 40]))
    obj.add_co_point("p1", "t1", np.array([70, 10]))
    obj.add_co_point("p1", "t3", np.array([50, 90]))
    id_pt = ["p0", "p0", "p1", "p1"]
    id_img = ["t1", "t2", "t1", "t3"]
    c = [51, 41, 71, 51]
    lin = [27, 38, 11, 89]
    pd_mes = pd.DataFrame({"id_pt": id_pt, "id_img": id_img, "column": c, "line": lin})
    obj.set_point_image_dataframe(pd_mes, "co_points")
    assert (obj.shots["t1"].co_points["p0"] == np.array([51, 27])).all()
    assert (obj.shots["t1"].co_points["p1"] == np.array([71, 11])).all()
    assert (obj.shots["t2"].co_points["p0"] == np.array([41, 38])).all()
    assert (obj.shots["t3"].co_points["p1"] == np.array([51, 89])).all()


def test_get_point_world_dataframe_copoints():
    obj = Worksite("Test")
    obj.co_pts_world = {"a": np.array([10, 20, 30]),
                        "b": np.array([40, 90, 10]),
                        "c": np.array([30, 60, 20])}
    pd_pt = obj.get_point_world_dataframe("co_points", [])
    assert (pd_pt["id_pt"].to_numpy() == np.array(["a", "b", "c"])).all()
    assert (pd_pt["x"].to_numpy() == np.array([10, 40, 30])).all()
    assert (pd_pt["y"].to_numpy() == np.array([20, 90, 60])).all()
    assert (pd_pt["z"].to_numpy() == np.array([30, 10, 20])).all()


def test_set_param_shot():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.set_proj(EPSGFR, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.set_param_shot()
    assert (work.shots["shot1"].pos_shot_eucli != np.array([None, None, None])).all()
    assert work.shots["shot1"].z_nadir is not None


def test_set_param_shot_noprojengineandtypediff():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.set_proj(EPSGAR)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    with pytest.raises(ValueError):
        work.set_param_shot()


def test_set_param_shot_noprojengineandsametype():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.set_proj(EPSGAR)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "height"
    work.type_z_data = "height"
    with pytest.raises(ValueError):
        work.set_param_shot()


def test_set_param_shot_nodtm():
    Dtm.clear()
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.set_proj(EPSGFR, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_param_shot()
    assert (work.shots["shot1"].pos_shot_eucli != np.array([None, None, None])).all()
    assert work.shots["shot1"].z_nadir is None


def test_set_unit_output():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.set_proj(EPSGFR, LIST_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.set_param_shot(approx=False)
    work.set_unit_output("height", "radian", linear_alteration=False)
    assert work.shots["shot1"].unit_angle == "radian"
    assert work.shots["shot1"].linear_alteration is False
    assert (work.shots["shot1"].ori_shot == np.array([np.pi, 0, 2*np.pi])).all()
    assert work.type_z_shot == "height"


def test_set_unit_output_sameunit():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_unit_output("altitude", "degree", linear_alteration=True)
    assert work.shots["shot1"].unit_angle == "degree"
    assert work.shots["shot1"].linear_alteration
    assert (work.shots["shot1"].ori_shot == np.array([180, 0, 360])).all()
    assert work.type_z_shot == "altitude"


def test_set_unit_output_changeorder():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_unit_output(order_axe="pok")
    assert (work.shots["shot1"].ori_shot != np.array([180, 0, 360])).all()


def test_set_unit_output_changeproj():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([657945.43, 6860369.44, 1771.280]),
                  np.array([180, 0, 360]), "cam_test", "degree", True, 'opk')
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.set_proj(EPSGFR, LIST_GEOID, 4326)
    work.set_unit_output()
    assert (np.round(work.shots["shot1"].pos_shot, 3) == [48.842, 2.427, 1771.280]).all()
