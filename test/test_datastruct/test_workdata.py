"""
Script test for module workdata
"""
import pytest
import pyproj
import numpy as np
import pandas as pd
from src.worksite.worksite import Worksite
from src.geodesy.proj_engine import ProjEngine
from src.datastruct.dtm import Dtm


PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def setup_module(module): # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_add_shot():
    obj = Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam", 'degree',True)
    assert obj.shots["test_shot"].name_shot == "test_shot"
    assert obj.shots["test_shot"].pos_shot[0] == 1
    assert obj.shots["test_shot"].pos_shot[1] == 2
    assert obj.shots["test_shot"].pos_shot[2] == 3
    assert obj.shots["test_shot"].ori_shot[0] == 3
    assert obj.shots["test_shot"].ori_shot[1] == 2
    assert obj.shots["test_shot"].ori_shot[2] == 1
    assert obj.shots["test_shot"].name_cam == "test_cam"


def test_set_proj_Lambertbase():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(2154, path_geotiff="./dataset/")
    work.set_param_shot(False)
    assert ProjEngine().projection_list == {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"], 'comment': 'Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93'}
    assert round(work.shots["t1"].projeucli.pt_central[0], 3) == 814975.925
    assert round(work.shots["t1"].projeucli.pt_central[1], 3) == 6283986.148


def test_set_proj_Lambertbase_pathfolder():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(2154, path_geotiff="dataset/")
    work.set_param_shot(False)
    assert ProjEngine().projection_list == {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"], 'comment': 'Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93'}
    assert round(work.shots["t1"].projeucli.pt_central[0], 3) == 814975.925
    assert round(work.shots["t1"].projeucli.pt_central[1], 3) == 6283986.148


def test_set_proj_Lambertbase_pathfolderwin():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(2154, path_geotiff="dataset\\")
    work.set_param_shot(False)
    assert ProjEngine().projection_list == {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"], 'comment': 'Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93'}
    assert round(work.shots["t1"].projeucli.pt_central[0], 3) == 814975.925
    assert round(work.shots["t1"].projeucli.pt_central[1], 3) == 6283986.148


def test_set_proj_Lambertbase_withEPSG():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([814975.925, 6283986.148,1771.280]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(2154, "dataset/proj.json", "dataset/")
    work.set_param_shot(False)
    assert ProjEngine().projection_list == {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"], 'comment': 'Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93'}
    assert round(work.shots["t1"].projeucli.pt_central[0], 3) == 814975.925
    assert round(work.shots["t1"].projeucli.pt_central[1], 3) == 6283986.148


def test_set_proj_withjsonandepsg():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(4339, "dataset/proj.json")
    work.set_param_shot(False)
    assert ProjEngine().projection_list == {"geoc": "EPSG:4340", "geog": "EPSG:4176", "comment": "Projection of Australian Antartic"}
    assert work.shots["t1"].projeucli.pt_central[0] == 1
    assert work.shots["t1"].projeucli.pt_central[1] == 2


def test_set_proj_epsgnojson():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(4339)
    assert ProjEngine().epsg == 4339


def test_set_proj_otherepsgandnotgoodjson():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.set_proj(4326, "dataset/proj.json")
    assert ProjEngine().epsg == 4326


def test_set_proj_badepsg():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    with pytest.raises(pyproj.exceptions.CRSError) as e_info:
        work.set_proj(1111)


def test_set_proj_badepsg2():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    with pytest.raises(pyproj.exceptions.CRSError) as e_info:
        work.set_proj(1111)


def test_add_cam():
    obj = Worksite(name = "Test")
    obj.add_camera("test_cam", 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    assert obj.cameras["test_cam"].name_camera == "test_cam"
    assert obj.cameras["test_cam"].ppax == 13210.00
    assert obj.cameras["test_cam"].ppay == 8502.00
    assert obj.cameras["test_cam"].focal == 30975.00


def test_add_co_point():
    obj = Worksite(name = "Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_co_point("p0", "t1", 50, 30)
    obj.add_co_point("p0", "t2", 40, 40)
    obj.add_co_point("p1", "t1", 70, 10)
    obj.add_co_point("p1", "t3", 50, 90)
    assert obj.co_points["p0"] == ["t1", "t2"]
    assert obj.co_points["p1"] == ["t1", "t3"]
    assert obj.shots["t1"].co_points["p0"] == [50, 30]
    assert obj.shots["t1"].co_points["p1"] == [70, 10]
    assert obj.shots["t2"].co_points["p0"] == [40, 40]
    assert obj.shots["t3"].co_points["p1"] == [50, 90]


def test_add_ground_img_pt():
    obj = Worksite(name = "Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_ground_img_pt("p0", "t1", 50, 30)
    obj.add_ground_img_pt("p0", "t2", 40, 40)
    obj.add_ground_img_pt("p1", "t1", 70, 10)
    obj.add_ground_img_pt("p1", "t3", 50, 90)
    assert obj.ground_img_pts["p0"] == ["t1", "t2"]
    assert obj.ground_img_pts["p1"] == ["t1", "t3"]
    assert obj.shots["t1"].ground_img_pts["p0"] == [50, 30]
    assert obj.shots["t1"].ground_img_pts["p1"] == [70, 10]
    assert obj.shots["t2"].ground_img_pts["p0"] == [40, 40]
    assert obj.shots["t3"].ground_img_pts["p1"] == [50, 90]


def test_add_gcp():
    obj = Worksite(name = "Test")
    obj.add_gcp('"1003"', 13, np.array([1,2,3]))
    assert obj.gcps['"1003"'].name_gcp == '"1003"'
    assert obj.gcps['"1003"'].code == 13
    assert (obj.gcps['"1003"'].coor == np.array([1,2,3])).all()


def test_set_z_nadir_shot():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test',"degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.set_param_shot(False)
    assert work.shots["shot_test"].z_nadir


def test_set_dtm():
    work = Worksite("Test")
    work.set_dtm(PATH_DTM, "height")
    dtm = Dtm()
    assert dtm.type_dtm == "height"
    assert dtm.order == 1
    assert dtm.keep_in_memory == False
    assert hasattr(dtm, 'img')
    assert hasattr(dtm, 'rb')
    assert hasattr(dtm, 'gt')


def test_set_unit_shot():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True)
    work.set_proj(2154, "dataset/proj.json", "./dataset/")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.set_param_shot(False)
    work.set_unit_shot("height", "radian", False)
    assert work.shots["shot1"].unit_angle == "radian"
    assert work.shots["shot1"].linear_alteration == False
    assert (work.shots["shot1"].ori_shot == np.array([np.pi,0,2*np.pi])).all()
    assert work.type_z_shot == "height"


def test_set_unit_shot_sameunit():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([180,0,360]),"cam_test","degree",True)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460.00, 17004.00)
    work.type_z_shot = "altitude"
    work.set_unit_shot("altitude", "degree", True)
    assert work.shots["shot1"].unit_angle == "degree"
    assert work.shots["shot1"].linear_alteration == True
    assert (work.shots["shot1"].ori_shot == np.array([180,0,360])).all()
    assert work.type_z_shot == "altitude"


def test_get_point_panda_copoints():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_co_point("p0", "t1", 50, 30)
    obj.add_co_point("p0", "t2", 40, 40)
    obj.add_co_point("p1", "t1", 70, 10)
    obj.add_co_point("p1", "t3", 50, 90)
    pd = obj.get_point_image_pandas("co_points", [])
    assert (pd["id_pt"].to_numpy() == np.array(["p0", "p0", "p1", "p1"])).all()
    assert (pd["id_img"].to_numpy() == np.array(["t1","t2","t1","t3"])).all()
    assert (pd["column"].to_numpy() == np.array([50,40,70,50])).all()
    assert (pd["line"].to_numpy() == np.array([30,40,10,90])).all()


def test_get_point_panda_groundimgpt():
    obj = Worksite("Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam","degree",True)
    obj.add_ground_img_pt("p0", "t1", 50, 30)
    obj.add_ground_img_pt("p0", "t2", 40, 40)
    obj.add_ground_img_pt("p1", "t1", 70, 10)
    obj.add_ground_img_pt("p1", "t3", 50, 90)
    obj.add_gcp('p0', 13, np.array([1,2,3]))
    obj.add_gcp('p1', 3, np.array([1,2,3]))
    pd = obj.get_point_image_pandas("ground_img_pts", [13])
    assert (pd["id_pt"].to_numpy() == np.array(["p0", "p0"])).all()
    assert (pd["id_img"].to_numpy() == np.array(["t1","t2"])).all()
    assert (pd["column"].to_numpy() == np.array([50,40])).all()
    assert (pd["line"].to_numpy() == np.array([30,40])).all()


def test_set_point_panda():
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
    obj.set_point_image_pandas(pd_mes, "co_points")
    assert (obj.shots["t1"].co_points["p0"] == np.array([51, 27])).all()
    assert (obj.shots["t1"].co_points["p1"] == np.array([71, 11])).all()
    assert (obj.shots["t2"].co_points["p0"] == np.array([41, 38])).all()
    assert (obj.shots["t3"].co_points["p1"] == np.array([51, 89])).all()


def test_get_point_world_panda_copoints():
    obj = Worksite("Test")
    obj.co_pts_world = {"a": np.array([10,20,30]),
                        "b": np.array([40,90,10]),
                        "c": np.array([30,60,20]),}
    pd = obj.get_point_world_pandas("co_points", [])
    assert (pd["id_pt"].to_numpy() == np.array(["a", "b", "c"])).all()
    assert (pd["x"].to_numpy() == np.array([10,40,30])).all()
    assert (pd["y"].to_numpy() == np.array([20,90,60])).all()
    assert (pd["z"].to_numpy() == np.array([30,10,20])).all()