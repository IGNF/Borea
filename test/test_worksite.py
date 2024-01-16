"""
Script test for module worksite
"""
import numpy as np
from src.datastruct.worksite import Worksite


def test_add_shot():
    obj = Worksite(name = "Test")
    obj.add_shot("test_shot", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
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
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:2154")
    assert work.proj.projection_list == {'geoc': 'EPSG:4964', 'geog': 'EPSG:7084', "geoid": ["fr_ign_RAF20"], 'comment': 'Projection of French metropolis : Systeme=RGF93 - Projection=Lambert93'}
    assert work.projeucli.x_central == 1
    assert work.projeucli.y_central == 2


def test_set_proj_withjsonandepsg():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:4339", "test/data/proj.json")
    assert work.proj.projection_list == {"geoc": "EPSG:4340", "geog": "EPSG:4176", "geoid": ["au_ga_AGQG_20201120"], "comment": "Projection of Australian Antartic"}
    assert work.projeucli.x_central == 1
    assert work.projeucli.y_central == 2


def test_set_proj_epsgnojson():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:4339")
    assert work.proj.epsg == "EPSG:4339"


def test_set_proj_otherepsgandnotgoodjson():
    work = Worksite(name = "Test")
    work.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    work.set_proj("EPSG:4326", "test/data/proj.json")
    assert work.proj.epsg == "EPSG:4326"


def test_add_cam():
    obj = Worksite(name = "Test")
    obj.add_camera("test_cam", 13210.00, 8502.00, 30975.00)
    assert obj.cameras["test_cam"].name_camera == "test_cam"
    assert obj.cameras["test_cam"].ppax == 13210.00
    assert obj.cameras["test_cam"].ppay == 8502.00
    assert obj.cameras["test_cam"].focal == 30975.00


def test_add_copoint():
    obj = Worksite(name = "Test")
    obj.add_shot("t1", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    obj.add_shot("t2", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    obj.add_shot("t3", np.array([1,2,3]), np.array([3,2,1]), "test_cam")
    obj.add_copoint("p0", "t1", 50, 30)
    obj.add_copoint("p0", "t2", 40, 40)
    obj.add_copoint("p1", "t1", 70, 10)
    obj.add_copoint("p1", "t3", 50, 90)
    assert obj.copoints["p0"] == ["t1", "t2"]
    assert obj.copoints["p1"] == ["t1", "t3"]
    assert obj.shots["t1"].copoints["p0"] == [50, 30]
    assert obj.shots["t1"].copoints["p1"] == [70, 10]
    assert obj.shots["t2"].copoints["p0"] == [40, 40]
    assert obj.shots["t3"].copoints["p1"] == [50, 90]


def test_add_gcp():
    obj = Worksite(name = "Test")
    obj.add_gcp('"1003"', 13, np.array([1,2,3]))
    assert obj.gcps['"1003"'].name_gcp == '"1003"'
    assert obj.gcps['"1003"'].code == 13
    assert (obj.gcps['"1003"'].coor == np.array([1,2,3])).all()


def test_calculate_world_to_image_gcp_base():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_copoint('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.check_cop = True
    work.add_gcp('gcp_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.check_gcp = True
    work.calculate_world_to_image_gcp([3])
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 5
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 5
    assert len(work.shots['shot_test'].gcps) == 1


def test_calculate_world_to_image_gcp_addpointunknow():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_copoint('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.check_cop = True
    work.add_gcp('gcp_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp('gcp_test_test', 3, np.array([0,0,0]))
    work.check_gcp = True
    work.calculate_world_to_image_gcp([3])
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 5
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 5
    assert len(work.shots['shot_test'].gcps) == 1


def test_calculate_world_to_image_gcp_testcode():
    work = Worksite("test")
    work.add_shot("shot_test", np.array([814975.925, 6283986.148,1771.280]), np.array([-0.245070686036,-0.069409621323,0.836320989726]), 'cam_test')
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_copoint('gcp_test', 'shot_test', 24042.25, 14781.17)
    work.add_copoint('gcp_test_test', 'shot_test', 24042.25, 14781.17)
    work.check_cop = True
    work.add_gcp('gcp_test', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp('gcp_test_test', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.check_gcp = True
    work.calculate_world_to_image_gcp([13])
    assert abs(work.shots['shot_test'].gcps['gcp_test'][0] - 24042.25) < 5
    assert abs(work.shots['shot_test'].gcps['gcp_test'][1] - 14781.17) < 5
    assert len(work.shots['shot_test'].gcps) == 1


def test_barycentre():
    work = Worksite("Test")
    work.add_shot("shot1", np.array([1,8,2]), np.array([1,1,1]), 'cam_test')
    work.add_shot("shot2", np.array([3,6,6]), np.array([1,1,1]), 'cam_test')
    work.add_shot("shot3", np.array([2,8,10]), np.array([1,1,1]), 'cam_test')
    work.add_shot("shot4", np.array([2,10,14]), np.array([1,1,1]), 'cam_test')
    bary = work.calculate_barycentre()
    assert bary[0] == 2
    assert bary[1] == 8
    assert bary[2] == 8


def test_calculate_image_world_copoints():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_copoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_copoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_copoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.check_cop = True
    work.calculate_image_world_copoints()
    print(abs(work.cop_ground['"1003"'][0] - 815601.510),abs(work.cop_ground['"1003"'][1] - 6283629.280),abs(work.cop_ground['"1003"'][2] - 54.960))
    assert abs(work.cop_ground['"1003"'][0] - 815601.510) < 1300
    assert abs(work.cop_ground['"1003"'][1] - 6283629.280) < 228
    assert abs(work.cop_ground['"1003"'][2] - 54.960) < 100


def test_eucli_intersection_2p():
    work = Worksite("Test")
    work.add_shot("shot1",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("shot2",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_copoint('"1003"',"shot1",24042.25,14781.17)
    work.add_copoint('"1003"',"shot2",24120.2,10329.3)
    coor = work.eucli_intersection_2p('"1003"', work.shots["shot1"], work.shots["shot2"])
    actual = work.projeucli.euclidean_to_world(coor[0], coor[1], coor[2])
    print(abs(actual[0] - 815601.510),abs(actual[1] - 6283629.280),abs(actual[2] - 54.960))
    assert abs(actual[0] - 815601.510) < 1300
    assert abs(actual[1] - 6283629.280) < 500
    assert abs(actual[2] - 54.960) < 120

"""
def test_calculate_coor_ground_copoints2():
    work = Worksite("Test")
    work.add_shot("23FD1305x00026_01306",np.array([814975.925,6283986.148,1771.280]),np.array([-0.245070686036,-0.069409621323,0.836320989726]),"cam_test")
    work.add_shot("23FD1305x00026_01307",np.array([814977.593,6283733.183,1771.519]),np.array([-0.190175545509,-0.023695590794,0.565111690487]),"cam_test")
    work.add_shot("23FD1305x00026_01308",np.array([814978.586,6283482.827,1771.799]),np.array([-0.181570631296, 0.001583051432,0.493526899473]),"cam_test")
    work.set_proj("EPSG:2154")
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00)
    work.add_copoint('"1003"',"23FD1305x00026_01306",24042.25,14781.17)
    work.add_copoint('"1003"',"23FD1305x00026_01307",24120.2,10329.3)
    work.add_copoint('"1003"',"23FD1305x00026_01308",24161.49,5929.37)
    work.check_cop = True
    work.calculate_coor_ground_copoints2()
    print(abs(work.cop_ground['"1003"'][0] - 815601.510),abs(work.cop_ground['"1003"'][1] - 6283629.280),abs(work.cop_ground['"1003"'][2] - 54.960))
    assert abs(work.cop_ground['"1003"'][0] - 815601.510) < 1242
    assert abs(work.cop_ground['"1003"'][1] - 6283629.280) < 228
    assert abs(work.cop_ground['"1003"'][2] - 54.960) < 41
"""