"""
Script test for module worksite
"""
import numpy as np
import pandas as pd
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


def test_get_copts_img_world():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_co_point("la", "shot1", 10, 10)
    work.add_co_point("do", "shot1", 50, 14)
    work.co_pts_world["la"] = np.array([20, 30, 50])
    work.co_pts_world["do"] = np.array([40, 35, 19])
    img, world = work.get_points_shot_numpy("shot1", "co_points")
    assert (img == np.array([[10, 50], [10, 14]])).all()
    assert (world == np.array([[20, 40], [30, 35], [50, 19]])).all()


def test_get_gcp_img_world():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test',"degree",True)
    work.add_gcp2d("la", "shot1", 10, 10)
    work.add_gcp2d("do", "shot1", 50, 14)
    work.gcp2d_in_world["la"] = np.array([20, 30, 50])
    work.gcp2d_in_world["do"] = np.array([40, 35, 19])
    img, world = work.get_points_shot_numpy("shot1", "gcp2d")
    assert (img == np.array([[10, 50], [10, 14]])).all()
    assert (world == np.array([[20, 40], [30, 35], [50, 19]])).all()


def test_get_point_dataframe_copoints():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_co_point("p0", "t1", 50, 30)
    obj.add_co_point("p0", "t2", 40, 40)
    obj.add_co_point("p1", "t1", 70, 10)
    obj.add_co_point("p1", "t3", 50, 90)
    pd = obj.get_point_image_dataframe("co_points", [])
    assert (pd["id_pt"].to_numpy() == np.array(["p0", "p0", "p1", "p1"])).all()
    assert (pd["id_img"].to_numpy() == np.array(["t1","t2","t1","t3"])).all()
    assert (pd["column"].to_numpy() == np.array([50,40,70,50])).all()
    assert (pd["line"].to_numpy() == np.array([30,40,10,90])).all()


def test_get_point_dataframe_groundimgpt():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_gcp2d("p0", "t1", 50, 30)
    obj.add_gcp2d("p0", "t2", 40, 40)
    obj.add_gcp2d("p1", "t1", 70, 10)
    obj.add_gcp2d("p1", "t3", 50, 90)
    obj.add_gcp('p0', 13, np.array([1,2,3]))
    obj.add_gcp('p1', 3, np.array([1,2,3]))
    pd = obj.get_point_image_dataframe("gcp2d", [13])
    assert (pd["id_pt"].to_numpy() == np.array(["p0", "p0"])).all()
    assert (pd["id_img"].to_numpy() == np.array(["t1","t2"])).all()
    assert (pd["column"].to_numpy() == np.array([50,40])).all()
    assert (pd["line"].to_numpy() == np.array([30,40])).all()


def test_set_point_dataframe():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_co_point("p0", "t1", 50, 30)
    obj.add_co_point("p0", "t2", 40, 40)
    obj.add_co_point("p1", "t1", 70, 10)
    obj.add_co_point("p1", "t3", 50, 90)
    id_pt = ["p0", "p0", "p1", "p1"]
    id_img = ["t1","t2","t1","t3"]
    c = [51,41,71,51]
    l = [27,38,11,89]
    pd_mes = pd.DataFrame({"id_pt": id_pt, "id_img": id_img, "column": c, "line": l})
    obj.set_point_image_dataframe(pd_mes, "co_points")
    assert (obj.shots["t1"].co_points["p0"] == np.array([51, 27])).all()
    assert (obj.shots["t1"].co_points["p1"] == np.array([71, 11])).all()
    assert (obj.shots["t2"].co_points["p0"] == np.array([41, 38])).all()
    assert (obj.shots["t3"].co_points["p1"] == np.array([51, 89])).all()


def test_get_point_world_dataframe_copoints():
    obj = Worksite("Test")
    obj.co_pts_world = {"a": np.array([10,20,30]),
                        "b": np.array([40,90,10]),
                        "c": np.array([30,60,20]),}
    pd = obj.get_point_world_dataframe("co_points", [])
    assert (pd["id_pt"].to_numpy() == np.array(["a", "b", "c"])).all()
    assert (pd["x"].to_numpy() == np.array([10,40,30])).all()
    assert (pd["y"].to_numpy() == np.array([20,90,60])).all()
    assert (pd["z"].to_numpy() == np.array([30,10,20])).all()
