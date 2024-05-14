"""
Example to use transformation image to world. (main ligne 139)
"""
# pylint: disable=import-error, missing-function-docstring
# pylint: disable=wrong-import-position, pointless-string-statement
import sys
import os
import numpy as np
from eg_build_worksite_by_data import worksite_1shot, worksite_2shots_2copts
# pylint: disable-next=unused-import, line-too-long
from eg_build_worksite_by_file import worksite_opk, worksite_add_co_points, worksite_add_gcp2d  # noqa: F401, E501

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.worksite.worksite import Worksite  # noqa: E402
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot  # noqa: E402
# pylint: disable-next=line-too-long
from borea.transform_world_image.transform_worksite.image_world_work import ImageWorldWork  # noqa: E402, E501
from borea.writer.writer_df_to_txt import write_df_to_txt  # noqa: E402


OUTPUT_PATH = "./test/tmp"


def image_to_world_one_point(point2d: np.ndarray) -> np.ndarray:
    # Build worksite with one shot
    work_1shot = worksite_1shot()

    # Settup type z data in output "height", "altitude" or None
    # If None type_z_data = type_z_shot
    work_1shot.set_type_z_data("height")

    coor3d = ImageWorldShot(work_1shot.shots["shot1"],
                            work_1shot.cameras[list(work_1shot.cameras.keys())[0]]
                            ).image_to_world(point2d,
                                             work_1shot.type_z_data,
                                             work_1shot.type_z_shot)

    return coor3d


def image_to_world_connecting_points_by_leastsquare() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height",
    if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite
    work_2shots_2copts = worksite_2shots_2copts()

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by least square.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work_2shots_2copts).manage_image_world("co_points", "square")

    # Return data
    return work_2shots_2copts


def image_to_world_connecting_points_by_intersection() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height",
    if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite
    work_2shots_2copts = worksite_2shots_2copts()

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by bundle intersection.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work_2shots_2copts).manage_image_world("co_points", "inter")

    # Return data
    return work_2shots_2copts


def image_to_world_connecting_points_by_leastsquare_file() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height",
    if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite with opk file
    work_opk = worksite_opk()

    # Add connecting point (co_point)
    work_opk = worksite_add_co_points(work_opk)
    # work = worksite_add_gcp2d(work)

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by least square.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work_opk).manage_image_world("co_points", "square")
    # ImageWorldWork(work).manage_image_world("gcp2d", "square")

    # Return data
    return work_opk


def image_to_world_connecting_points_by_intersection_file() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height",
    if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite with opk file
    work_opk = worksite_opk()

    # Add connecting point (co_point) or gcp2d
    work_opk = worksite_add_co_points(work_opk)
    # work = worksite_add_gcp2d(work)

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by bundle intersection.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work_opk).manage_image_world("co_points", "inter")
    # ImageWorldWork(work).manage_image_world("gcp2d", "inter")

    # Return data
    return work_opk


if __name__ == "__main__":
    # Creation of folder
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    #################################
    #   For one point and one Shot  #
    #################################

    # Transform image coodinates in terrain coordinates for one point and one shot.
    print("\nTransformation of one point")
    # Image coordinates of the point (dim image 26460 x 17004)
    pt2d = np.array([24042.25, 14781.17])
    coors = image_to_world_one_point(pt2d)
    print('Terrain coordinates of the point '
          f'{pt2d} is X: {coors[0]} Y: {coors[1]} Z: {coors[2]}')

    #################################
    #  On worksite by least square  #
    #################################

    # Transform image coodinates in terrain coordinates of connecting points by least square.
    print("\nTransformation by least square one point")
    work = image_to_world_connecting_points_by_leastsquare()
    for name_pt, coors in work.co_pts_world.items():
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    print("\nTransformation by least square file of points")
    work = image_to_world_connecting_points_by_leastsquare_file()
    for name_pt, coors in work.co_pts_world.items():
    # for name_pt, coors in  work.gcp2d_in_world.items():  # noqa: E115
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    # This example make transformation in connecting point,
    # but you can make on gcp2d to replace "co_points" by "gcp2d" in type_point on
    # manage_image_world(), and return dictonary data with work.gcp2d_in_world.

    #################################
    #  On worksite by intersection  #
    #################################

    # Transform image coodinates in terrain coordinates of connecting points by intersection.
    print("\nTransformation by intersection one point")
    work = image_to_world_connecting_points_by_intersection()
    for name_pt, coors in work.co_pts_world.items():
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    print("\nTransformation by intersection file of points")
    work = image_to_world_connecting_points_by_intersection_file()
    for name_pt, coors in work.co_pts_world.items():
    # for name_pt, coors in  work.gcp2d_in_world.items():  # noqa: E115
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    # This example make transformation in connecting point,
    # but you can make on gcp2d to replace "co_points" by "gcp2d" in type_point on
    # manage_image_world(), and return dictonary data with work.gcp2d_in_world.

    #######################
    # Save transform data #
    #######################
    # Name of file output
    NAME_FILE = "image_world_pts"

    # Path of the save folder OUTPUT_PATH

    # Get data of calculate points in dataframe
    dataframe_pts = work.get_point_world_dataframe('co_points', [])  # or 'gcp2d'

    # Write data in txt
    print(f"\nSave data of transform coordiante in file: {OUTPUT_PATH}/{NAME_FILE}.txt")
    write_df_to_txt(NAME_FILE, OUTPUT_PATH, dataframe_pts)

    """ +++
    Transfoms image coordinates in terrain coordinates with filter in type of GCP.
    You need gcp3d informed in worksite.
    You just need to add a parameter to the manage_image_world function.

    ImageWorldWork(work).manage_image_world("gcp2d", "inter", [13])

    the last parameter, which is None by default and therefore takes all points,
    is a list of an element type which is the type of your GCP type.
    The calculation will therefore only be performed on gcp of type 13 here.
    You can put several GCP types in the list.
    """
