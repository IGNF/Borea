"""
Example to use transformation world to image. (main ligne 76)
"""
# pylint: disable=import-error, missing-function-docstring
# pylint: disable=wrong-import-position, pointless-string-statement
import sys
import os
import numpy as np
from eg_build_worksite_by_data import worksite_1shot, worksite_2shot_3gcp
from eg_build_worksite_by_file import worksite_opk, worksite_add_gcp3d, worksite_add_gcp2d0

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.worksite.worksite import Worksite  # noqa: E402
from borea.transform_world_image.transform_shot.world_image_shot import WorldImageShot  # noqa: E402
# pylint: disable-next=line-too-long
from borea.transform_world_image.transform_worksite.world_image_work import WorldImageWork  # noqa: E402, E501
from borea.writer.writer_df_to_txt import write_df_to_txt  # noqa: E402


OUTPUT_PATH = "./test/tmp"


def world_to_image_one_point(pt3d: np.ndarray) -> np.ndarray:
    # Build worksite with one shot
    work_1shot = worksite_1shot()

    # Settup type z data in input "height", "altitude" or None
    # If None type_z_data = type_z_shot
    work_1shot.set_type_z_data("height")

    coor2d = WorldImageShot(work_1shot.shots["shot1"],
                            work_1shot.cameras[list(work_1shot.cameras.keys())[0]]
                            ).world_to_image(pt3d,
                                             work_1shot.type_z_data,
                                             work_1shot.type_z_shot)

    return coor2d


def world_to_image_on_worksite_data() -> Worksite:
    # Build worksite
    work_2s3g = worksite_2shot_3gcp()

    # Calculate image coordinates
    WorldImageWork(work_2s3g).calculate_world_to_image([])

    # Return data
    return work_2s3g


def world_to_image_on_worksite_file() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height",
    if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite with opk file
    work_opk = worksite_opk()

    # Add ground control point terrain (gcp3d)
    work_opk = worksite_add_gcp3d(work_opk)

    # Add ground control point image with 0 in coordinates (gcp2d)
    # Used to find out in which image the points are located
    work_opk = worksite_add_gcp2d0(work_opk)

    # Calculate image coordinates
    WorldImageWork(work_opk).calculate_world_to_image([])

    # Return data
    return work_opk


if __name__ == "__main__":
    #################################
    #   For one point and one Shot  #
    #################################

    # Transform image coodinates in terrain coordinates for one point and one shot.
    print("\nTransformation of one point")
    # Image coordinates of the point (dim image 26460 x 17004)
    PT3D = np.array([815601.510, 6283629.280, 54.960])
    coors = world_to_image_one_point(PT3D)
    print(f'Image coordinates of the point {PT3D} is Column: {coors[0]} Line: {coors[1]}')

    #################################
    #       On worksite data        #
    #################################

    # Transform image coodinates in terrain coordinates of connecting points by least square.
    print("\nTransformation of a worksite data")
    work = world_to_image_on_worksite_data()
    print(work.get_point_image_dataframe("gcp3d"))

    #################################
    #        On worksite file       #
    #################################

    # Transform image coodinates in terrain coordinates of connecting points by intersection.
    print("\nTransformation of a worksite file")
    work = world_to_image_on_worksite_file()
    print(work.get_point_image_dataframe("gcp3d"))

    #######################
    # Save transform data #
    #######################
    # Name of file output
    NAME_FILE = "world_image_pts"

    # Path of the save folder OUTPUT_PATH

    # Get data of calculate points in dataframe
    dataframe_pts = work.get_point_image_dataframe('gcp2d')  # or 'co_point'

    # Write data in txt
    print(f"\nSave data of transform coordiante in file: {OUTPUT_PATH}/{NAME_FILE}.txt")
    write_df_to_txt(NAME_FILE, OUTPUT_PATH, dataframe_pts)

    """ +++
    Transfoms terrain coordinates in image coordinates with filter in type of GCP.
    You need gcp3d informed in worksite.
    You just need to add a parameter to the manage_image_world function.

    WorldImageWork(work).calculate_world_to_image([13])

    the last parameter, which is None by default and therefore takes all points,
    is a list of an element type which is the type of your GCP type.
    The calculation will therefore only be performed on gcp of type 13 here.
    You can put several GCP types in the list.
    """
