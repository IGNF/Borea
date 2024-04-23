"""
Example to use transformation world to image. (main ligne 72)
"""
import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__)[:-8], "implements/"))
from src.worksite.worksite import Worksite # type: ignore
from src.transform_world_image.transform_shot.world_image_shot import WorldImageShot # type: ignore
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork # type: ignore
from src.writer.writer_df_to_txt import write_df_to_txt # type: ignore

from eg_build_worksite_by_data import worksite_1shot, worksite_2shot_3gcp
from eg_build_worksite_by_file import worksite_opk, worksite_add_gcp3d, worksite_add_gcp2d0


OUTPUT_PATH = "./implements/test/tmp"


def world_to_image_one_point(pt3d: np.ndarray) -> np.ndarray:
    # Build worksite with one shot
    work = worksite_1shot()

    # Settup type z data in input "height", "altitude" or None
    # If None type_z_data = type_z_shot
    work.set_type_z_data("height")

    coor2d = WorldImageShot(work.shots["shot1"],
                            work.cameras[list(work.cameras.keys())[0]]
                            ).world_to_image(pt3d,
                                             work.type_z_data,
                                             work.type_z_shot)
    
    return coor2d


def world_to_image_on_worksite_data() -> Worksite:
    # Build worksite
    work = worksite_2shot_3gcp()

    # Calculate image coordinates
    WorldImageWork(work).calculate_world_to_image([])

    # Return data
    return work


def world_to_image_on_worksite_file() -> Worksite:
    """
    WARNING: You need minimum 2 shot and 2 same connecting points

    Unit of z output data is given by type_z_data "altitude" or "height", if is not instantiated he will take over the DTM unit.
    Here is "height".
    """
    # Build worksite with opk file
    work = worksite_opk()

    # Add ground control point terrain (gcp3d)
    work = worksite_add_gcp3d(work)

    # Add ground control point image with 0 in coordinates (gcp2d)
    # Used to find out in which image the points are located
    work = worksite_add_gcp2d0(work)

    # Calculate image coordinates
    WorldImageWork(work).calculate_world_to_image([])

    # Return data
    return work


if __name__ == "__main__":
    #################################
    #   For one point and one Shot  #
    #################################

    # Transform image coodinates in terrain coordinates for one point and one shot.
    print("\nTransformation of one point")
    # Image coordinates of the point (dim image 26460 x 17004)
    pt3d = np.array([815601.510, 6283629.280, 54.960])
    coor2d = world_to_image_one_point(pt3d)
    print(f'Image coordinates of the point {pt3d} is Column: {coor2d[0]} Line: {coor2d[1]}')


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
    name_file = "world_image_pts"

    # Path of the save folder
    path_folder = OUTPUT_PATH

    # Get data of calculate points in dataframe
    dataframe_pts = work.get_point_image_dataframe('gcp2d') # or 'co_point'

    # Write data in txt
    print(f"\nSave data of transform coordiante in file: {OUTPUT_PATH}/{name_file}.txt")
    write_df_to_txt(name_file, path_folder, dataframe_pts)


    """ +++
    Transfoms terrain coordinates in image coordinates with filter in type of GCP.
    You need gcp3d informed in worksite.
    You just need to add a parameter to the manage_image_world function.

    WorldImageWork(work).calculate_world_to_image([13])

    the last parameter, which is None by default and therefore takes all points, is a list of an element type which is the type of your GCP type.
    The calculation will therefore only be performed on gcp of type 13 here.
    You can put several GCP types in the list.
    """