"""
Example to use transformation image to world. (main ligne 132)
"""
import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__)[:-8], "implements/"))
from src.worksite.worksite import Worksite # type: ignore
from src.transform_world_image.transform_shot.image_world_shot import ImageWorldShot # type: ignore
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork # type: ignore
from src.writer.writer_df_to_txt import write_df_to_txt # type: ignore

from eg_build_worksite_by_data import worksite_1shot, worksite_2shots_2copts
from eg_build_worksite_by_file import worksite_opk, worksite_add_co_points, worksite_add_gcp2d


OUTPUT_PATH = "./implements/test/tmp"


def image_to_world_one_point(pt2d: np.ndarray) -> np.ndarray:
    # Build worksite with one shot
    work = worksite_1shot()

    # Settup type z data in output "height", "altitude" or None
    # If None type_z_data = type_z_shot
    work.set_type_z_data("height")

    coor3d = ImageWorldShot(work.shots["shot1"],
                            work.cameras[list(work.cameras.keys())[0]]
                            ).image_to_world(pt2d,
                                             work.type_z_data,
                                             work.type_z_shot)
    
    return coor3d


def image_to_world_connecting_points_by_leastsquare() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height", if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite
    work = worksite_2shots_2copts()

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by least square.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work).manage_image_world("co_points", "square")

    # Return data
    return work


def image_to_world_connecting_points_by_intersection() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height", if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite
    work = worksite_2shots_2copts()

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by bundle intersection.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work).manage_image_world("co_points", "inter")

    # Return data
    return work


def image_to_world_connecting_points_by_leastsquare_file() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height", if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite with opk file
    work = worksite_opk()

    # Add connecting point (co_point)
    work = worksite_add_co_points(work)
    # work = worksite_add_gcp2d(work)

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by least square.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work).manage_image_world("co_points", "square")
    # ImageWorldWork(work).manage_image_world("gcp2d", "square")


    # Return data
    return work


def image_to_world_connecting_points_by_intersection_file() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height", if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite with opk file
    work = worksite_opk()

    # Add connecting point (co_point) or gcp2d
    work = worksite_add_co_points(work)
    # work = worksite_add_gcp2d(work)

    # uncomment if you want to change the output z unit
    # work.set_type_z_data("altitude")

    # Calculate world coordinates by bundle intersection.
    # manage_image_world(type_point, type_process)
    ImageWorldWork(work).manage_image_world("co_points", "inter")
    # ImageWorldWork(work).manage_image_world("gcp2d", "inter")

    # Return data
    return work


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
    coor3d = image_to_world_one_point(pt2d)
    print(f'Terrain coordinates of the point {pt2d} is X: {coor3d[0]} Y: {coor3d[1]} Z: {coor3d[2]}')


    #################################
    #  On worksite by least square  #
    #################################

    # Transform image coodinates in terrain coordinates of connecting points by least square. 
    print("\nTransformation by least square one point")
    work = image_to_world_connecting_points_by_leastsquare()
    for name_pt, coors in  work.co_pts_world.items():
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    print("\nTransformation by least square file of points")
    work = image_to_world_connecting_points_by_leastsquare_file()
    for name_pt, coors in  work.co_pts_world.items():
    # for name_pt, coors in  work.gcp2d_in_world.items():
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    # This example make transformation in connecting point,
    # but you can make on gcp2d to replace "co_points" by "gcp2d" in type_point on manage_image_world(),
    # and return dictonary data with work.gcp2d_in_world.


    #################################
    #  On worksite by intersection  #
    #################################

    # Transform image coodinates in terrain coordinates of connecting points by intersection.
    print("\nTransformation by intersection one point")
    work = image_to_world_connecting_points_by_intersection()
    for name_pt, coors in  work.co_pts_world.items():
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")

    print("\nTransformation by intersection file of points")
    work = image_to_world_connecting_points_by_intersection_file()
    for name_pt, coors in  work.co_pts_world.items():
    # for name_pt, coors in  work.gcp2d_in_world.items():
        print(f"{name_pt} terrain coordinates X: {coors[0]} Y: {coors[1]} Z: {coors[2]}")
    
    # This example make transformation in connecting point,
    # but you can make on gcp2d to replace "co_points" by "gcp2d" in type_point on manage_image_world(),
    # and return dictonary data with work.gcp2d_in_world.

    #######################
    # Save transform data #
    #######################
    # Name of file output
    name_file = "image_world_pts"

    # Path of the save folder
    path_folder = OUTPUT_PATH

    # Get data of calculate points in dataframe
    dataframe_pts = work.get_point_world_dataframe('co_points', []) # or 'gcp2d'

    # Write data in txt
    print(f"\nSave data of transform coordiante in file: {OUTPUT_PATH}/{name_file}.txt")
    write_df_to_txt(name_file, path_folder, dataframe_pts)


    """ +++
    Transfoms image coordinates in terrain coordinates with filter in type of GCP.
    You need gcp3d informed in worksite.
    You just need to add a parameter to the manage_image_world function.

    ImageWorldWork(work).manage_image_world("gcp2d", "inter", [13])

    the last parameter, which is None by default and therefore takes all points, is a list of an element type which is the type of your GCP type.
    The calculation will therefore only be performed on gcp of type 13 here.
    You can put several GCP types in the list.
    """