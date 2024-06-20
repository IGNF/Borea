"""
Example to build worksite with data (main ligne 155)
"""
# pylint: disable=import-error, missing-function-docstring, wrong-import-position
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.worksite.worksite import Worksite  # noqa: E402


PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]
PATH_DTM = "./dataset/MNT_France_25m_h_crop.tif"


def worksite_1shot() -> Worksite:
    # Create worksite with just a name
    work = Worksite("Test")

    # Add two shots
    # Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration, order_axe)
    # unit_angle = "degree" or "radian".
    # linear_alteration True if z shot is corrected by linear alteration.
    # order of rotation axe "opk" or "pok" ...
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")

    # Settup the unit of z shot
    work.set_type_z_shot("altitude")

    # Setup projection
    # set_epsg(epsg, path_geoid)
    # the geoid is mandatory if type_z_data and type_z_shot are different
    work.set_proj(2154, PATH_GEOID)

    # Add camera information
    # add_camera(name_cam, ppax, ppay, focal, width, height)
    # ppax and ppay image center in pixel with distortion
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)

    # Add dtm to remove/add linear alteration or get z of a planimetric point
    # set_dtm(path_dtm, unit_of_dtm) unit is "altitude" or "height"
    work.set_dtm(PATH_DTM, "height")

    # Setup projection system of shot and z_nadir of shot
    work.set_param_shot()

    return work


def worksite_2shots_2copts() -> Worksite:
    # Create worksite with just a name
    work = Worksite("Test")

    # Add two shots
    # Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration, order_axe)
    # unit_angle = "degree" or "radian".
    # linear_alteration True if z shot is corrected by linear alteration.
    # order of rotation axe "opk" or "pok" ...
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("shot2", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")

    # Settup the unit of z shot
    work.set_type_z_shot("altitude")

    # Setup projection
    # set_epsg(epsg, path_geoid)
    # the geoid is mandatory if type_z_data and type_z_shot are different
    work.set_proj(2154, PATH_GEOID)

    # Add camera information
    # add_camera(name_cam, ppax, ppay, focal, width, height)
    # ppax and ppay image center in pixel with distortion
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)

    # Add connecting points in each shot
    # add_co_point(name_point, name_shot, np.array([column, line]))
    work.add_co_point('"1003"', "shot1", np.array([24042.25, 14781.17]))
    work.add_co_point('"1003"', "shot2", np.array([24120.2, 10329.3]))
    # you can do the same thing with gcp in images and gcp in the field.
    # work.add_gcp2d(name_point, name_shot, np.array([column, line]))
    # work.add_gcp3d(name_point, type_gcp, np.array([X, Y, Z]))
    # type_gcp is the code for whether it's a support or control point.

    # Add dtm to remove/add linear alteration or get z of a planimetric point
    # set_dtm(path_dtm, unit_of_dtm) unit is "altitude" or "height"
    work.set_dtm(PATH_DTM, "height")

    # Setup projection system of shot and z_nadir of shot
    work.set_param_shot()

    return work


def worksite_2shot_3gcp() -> Worksite:
    # Create worksite with just a name
    work = Worksite("Test")

    # Add two shots
    # Shot(name_shot, [X, Y, Z], [O, P, K], name_cam, unit_angle, linear_alteration, order_axe)
    # unit_angle = "degree" or "radian".
    # linear_alteration True if z shot is corrected by linear alteration.
    # order of rotation axe "opk" or "pok" ...
    work.add_shot("shot1", np.array([814975.925, 6283986.148, 1771.280]),
                  np.array([-0.245070686036, -0.069409621323, 0.836320989726]),
                  "cam_test", "degree", True, "opk")
    work.add_shot("shot2", np.array([814977.593, 6283733.183, 1771.519]),
                  np.array([-0.190175545509, -0.023695590794, 0.565111690487]),
                  "cam_test", "degree", True, "opk")

    # Settup the unit of z shot
    work.set_type_z_shot("altitude")

    # Setup projection
    # set_epsg(epsg, path_geoid)
    # the geoid is mandatory if type_z_data and type_z_shot are different
    work.set_proj(2154, PATH_GEOID)

    # Add camera information
    # add_camera(name_cam, ppax, ppay, focal, width, height,)
    # ppax and ppay image center in pixel with distortion
    work.add_camera('cam_test', 13210.00, 8502.00, 30975.00, 26460, 17004)

    # Add connecting points
    # add_gcp2d(name_point, name_shot, column, line)
    work.add_gcp2d('gcp1', 'shot1', np.array([0, 0]))
    work.add_gcp2d('gcp2', 'shot1', np.array([0, 0]))
    work.add_gcp2d('gcp3', 'shot2', np.array([0, 0]))

    # Add gcps points
    # add_gcp3d(name_gcp, code, coor)
    work.add_gcp3d('gcp1', 13, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('gcp2', 3, np.array([815601.510, 6283629.280, 54.960]))
    work.add_gcp3d('gcp3', 13, np.array([815601.510, 6283629.280, 54.960]))

    # Settup unit z of gcp "height" or "altitude"
    work.set_type_z_data("height")

    # Add dtm to remove/add linear alteration or get z of a planimetric point
    # set_dtm(path_dtm, unit_of_dtm) unit is "altitude" or "height"
    work.set_dtm(PATH_DTM, "height")

    # Setup projection system of shot and z_nadir of shot
    work.set_param_shot()

    return work


if __name__ == "__main__":
    # Build worksite with just one shot
    work1 = worksite_1shot()

    # Build worksite with 2 shots and 2 connecting points
    work2 = worksite_2shots_2copts()

    # Build worksite with 2 shots and 3 gcp3d and 3 gcp2d0
    work3 = worksite_2shot_3gcp()
