"""
Script test for module shot_pos
"""
# pylint: disable=import-error, missing-function-docstring
import numpy as np
from src.worksite.worksite import Worksite
from src.datastruct.camera import Camera
from src.datastruct.shot import Shot
from src.geodesy.proj_engine import ProjEngine
from src.transform_world_image.transform_worksite.space_resection import SpaceResection
from src.datastruct.dtm import Dtm
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_point import read_file_pt, read_file_pt_dataframe


INPUT_OPK = "./dataset/23FD1305_alt_test.OPK"
INPUT_OPK2 = "./test/data/dataset2/23FD1305_alt_2.OPK"
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]
PATH_CAM = ["./dataset/Camera1.txt"]
PT_LIAISON = "./dataset/liaisons_test.mes"
PT_LIAISON2 = "./test/data/dataset2/all_liaisons2.mes"
PT_LIAISON0 = "./test/data/dataset2/all_liaisons2_world.mes"


def dtm_singleton(path, type_dtm):
    Dtm.clear()
    Dtm().set_dtm(path, type_dtm)


def proj_singleton(epsg, path_geoid=None):
    ProjEngine.clear()
    ProjEngine().set_epsg(epsg, path_geoid)


def test_shootings_position():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("23FD1305x00026_01307", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")
    work.set_proj(2154, PATH_GEOID)
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.set_dtm(PATH_DTM, "height")
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    work.set_param_shot()
    SpaceResection(work).space_resection_on_worksite()
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[0] - 814975.925) < 0.02
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[1] - 6283986.148) < 0.02
    assert abs(work.shots["23FD1305x00026_01306"].pos_shot[2] - 1771.280) < 0.02
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[0] - 814977.593) < 0.02
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[1] - 6283733.183) < 0.02
    assert abs(work.shots["23FD1305x00026_01307"].pos_shot[2] - 1771.519) < 0.02


def test_space_resection():
    shot = Shot("test_shot", np.array([814975.925, 6283986.148, 1771.280]),
                np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                "test_cam", "degree", True, "opk")
    cam = Camera("test_cam", 13210.00, 8502.00, 30975.00, 26460, 17004)
    proj_singleton(2154, PATH_GEOID)
    dtm_singleton(PATH_DTM, "height")
    shot.set_param_eucli_shot(approx=False)
    z_nadir = ImageWorldShot(shot, cam).image_to_world(np.array([cam.ppax, cam.ppay]),
                                                       'altitude', 'altitude', False)[2]
    shot.set_z_nadir(z_nadir)
    work = Worksite("Test")
    work.add_camera('test_cam', 13210.00, 8502.00, 30975.00, 26460, 17004)
    work.type_z_shot = "altitude"
    work.type_z_data = "height"
    actual_shot = SpaceResection(work).space_resection_gap(shot)
    assert abs(actual_shot.pos_shot[0] - 814975.925) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283986.148) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1771.280) < 0.02


def test_take_obs():
    work = reader_orientation(INPUT_OPK,
                              {"order_axe": 'opk',
                               "interval": [2, None],
                               "header": list("NXYZOPKC"),
                               "unit_angle": "degree",
                               "linear_alteration": True})
    work.set_proj(2154, PATH_GEOID)
    read_camera(PATH_CAM, work)
    work.set_dtm(PATH_DTM, "height")
    work.set_param_shot()
    read_file_pt(PT_LIAISON, list("PNXY"), "co_point", work)
    actual_obs, actual_ptw = SpaceResection(work).take_obs(work.shots["23FD1305x00026_01306"])
    assert (actual_obs[:, 0:3] == np.array([[3885.75, 6033.01, 3896.99],
                                            [14969.14, 16208.41, 13858.47]])).all()
    assert (np.round(actual_ptw[:, 0:3], 0) == np.array([[814451, 814574, 814450],
                                                         [6283601, 6283532, 6283665],
                                                         [401, 399, 401]])).all()


def test_space_resection_othershot():
    work = reader_orientation(INPUT_OPK2,
                              {"order_axe": 'opk',
                               "interval": [2, None],
                               "header": list("NXYZOPKC"),
                               "unit_angle": "degree",
                               "linear_alteration": True})
    work.set_proj(2154, PATH_GEOID)
    read_camera(PATH_CAM, work)
    work.set_dtm(PATH_DTM, "height")
    work.set_param_shot()
    actual_shot = SpaceResection(work).space_resection_gap(work.shots["23FD1305x00054_05677"])
    assert abs(actual_shot.pos_shot[0] - 833127.599) < 0.02
    assert abs(actual_shot.pos_shot[1] - 6283057.326) < 0.02
    assert abs(actual_shot.pos_shot[2] - 1765.554) < 0.02


def test_space_resection_withcopoints():
    work = reader_orientation(INPUT_OPK2,
                              {"order_axe": 'opk',
                               "interval": [2, None],
                               "header": list("NXYZOPKC"),
                               "unit_angle": "degree",
                               "linear_alteration": True})
    work.set_proj(2154, PATH_GEOID)
    read_camera(PATH_CAM, work)
    work.set_dtm(PATH_DTM, "height")
    work.set_param_shot()
    read_file_pt(PT_LIAISON2, list("PNXY"), "co_point", work)
    SpaceResection(work).space_resection_gap(work.shots["23FD1305x00054_05677"])
    SpaceResection(work).space_resection_on_worksite()
    assert abs(work.shots["23FD1305x00054_05677"].pos_shot[0] - 833127.599) < 0.02
    assert abs(work.shots["23FD1305x00054_05677"].pos_shot[1] - 6283057.326) < 0.02
    assert abs(work.shots["23FD1305x00054_05677"].pos_shot[2] - 1765.554) < 0.02
    assert abs(work.shots["23FD1305x00027_01475"].pos_shot[0] - 815631.723) < 0.02
    assert abs(work.shots["23FD1305x00027_01475"].pos_shot[1] - 6278954.522) < 0.02
    assert abs(work.shots["23FD1305x00027_01475"].pos_shot[2] - 1762.738) < 0.02


def test_space_resection_to_worksite():
    work = Worksite("Test")
    work.set_proj(2154, PATH_GEOID)
    read_camera(PATH_CAM, work)
    work.set_dtm(PATH_DTM, "height")
    pt2d = read_file_pt_dataframe(PT_LIAISON2, list("PNXY"), "pt2d")
    pt3d = read_file_pt_dataframe(PT_LIAISON0, list("PXYZ"), "pt3d")
    work.type_z_data = "height"
    work.type_z_shot = "altitude"
    work.approxeucli = False
    pinit = {"coor_init": np.array([825439, 6289034, 1500])}
    SpaceResection(work).space_resection_to_worksite(pt2d, pt3d, pinit)
    assert (work.shots["23FD1305x00027_01495"].pos_shot -
            np.array([815630.519, 6283987.569, 1760.904]) < 0.01).all()
    assert (work.shots["23FD1305x00027_01495"].ori_shot -
            np.array([0.213018802034, -0.005320804811, 179.933728024748]) < 0.001).all()
    assert (work.shots["23FD1305x00054_05677"].pos_shot -
            np.array([833127.599, 6283057.326, 1765.554]) < 0.01).all()
    assert (work.shots["23FD1305x00054_05677"].ori_shot -
            np.array([-0.199659691541, -0.040545179521, 0.005516407740]) < 0.001).all()
    assert (work.shots["23FD1305x00055_05930"].pos_shot -
            np.array([833783.266, 6281039.022, 1769.374]) < 0.05).all()
    assert (work.shots["23FD1305x00055_05930"].ori_shot -
            np.array([0.244624422382, -0.032710653706, -178.344546125459]) < 0.002).all()


def test_init_kappa():
    work = Worksite("Test")
    pt2d = read_file_pt_dataframe(PT_LIAISON2, list("PNXY"), "pt2d")
    pt3d = read_file_pt_dataframe(PT_LIAISON0, list("PXYZ"), "pt3d")
    kappa = []
    for name_shot, group in pt2d.groupby("id_shot"):
        if name_shot not in ["23FD1305x00027_01495", "23FD1305x00054_05677",
                             "23FD1305x00055_05930"]:
            continue
        if group.shape[0] < 3:
            continue

        dfm = group.merge(pt3d, how="inner", on="id_pt")

        kappa.append(SpaceResection(work).init_kappa(dfm))
    assert kappa[0] == 179
    assert kappa[1] == 0
    assert kappa[2] == 179
