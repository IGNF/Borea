"""
Example to use transformation data with space resection. (main ligne 67)
"""
# pylint: disable=import-error, missing-function-docstring
# pylint: disable=wrong-import-position, pointless-string-statement
import sys
import os
import numpy as np
from eg_build_worksite_by_file import worksite_opk, worksite_without_shot

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.worksite.worksite import Worksite  # noqa: E402
# pylint: disable-next=line-too-long
from src.transform_world_image.transform_worksite.space_resection import SpaceResection  # noqa: E402, E501
from src.reader.reader_point import read_file_pt_dataframe  # noqa: E402


PATH_CO_PT_IMAGE = "./test/data/dataset2/all_liaisons2.mes"
PATH_CO_PT_WORLD = "./test/data/dataset2/all_liaisons2_world.mes"


def space_resection_add_gap(gap: tuple) -> Worksite:
    """
    Function for recalculating the 6 external parameters of acquisitions
    (X, Y, Z position and omega, phi, kappa orientation)
    by adding a deviation to the position of points in the image to perform
    a transformation and change of reference frame.
    """
    # Build a worksite
    work_opk = worksite_opk()

    # Make space resection on known shot with adding a gap
    SpaceResection(work_opk).space_resection_on_worksite(add_pixel=gap)

    return work_opk


def space_resection_on_points_to_shot() -> Worksite:
    """
    Function for calculating 6 external acquisition parameters
    (X, Y, Z position and omega, phi, kappa orientation)
    from a set of image and terrain points.
    """
    # Build worksite with camera, projection and dtm
    work_noshot = worksite_without_shot()

    # Read file of point to have in DataFrame format
    # read_file_pt_dataframe(path_file, header_file, type_point = choices([pt2d, pt3d])
    pt2d = read_file_pt_dataframe(PATH_CO_PT_IMAGE, list("PNXY"), "pt2d")
    pt3d = read_file_pt_dataframe(PATH_CO_PT_WORLD, list("PXYZ"), "pt3d")

    # Setup unit z data, shot in worksite and euclidean system to use for shot
    work_noshot.set_type_z_data("height")
    work_noshot.set_type_z_shot("altitude")
    work_noshot.set_approx_eucli_proj(False)

    # A dictionary with one balise "coor_init": array of 3D point with X and Y a
    # point within the construction site and Z the aircraft flying altitude or height.
    pinit = {"coor_init": np.array([825439, 6289034, 1500])}

    # Make space resection on point to calcul 6 external parameters of shots
    SpaceResection(work_noshot).space_resection_to_worksite(pt2d, pt3d, pinit)

    return work_noshot


if __name__ == "__main__":
    #################################
    #   Space resection with a gap  #
    #################################
    print("\nMake space resection on known shot with a gap.")
    print("Original file of opk is: ./dataset/23FD1305_alt_test.OPK\n")
    # Gap in pixel to add in position of image point
    GAP = (0, 0)
    # Make calculation
    work = space_resection_add_gap(GAP)
    for name_shot, shot in work.shots.items():
        print(f"Shot {name_shot} with a gap {GAP} are position: "
              f"{shot.pos_shot} and orientation {shot.ori_shot}")

    ########################################
    #   Space resection to build worksite  #
    ########################################
    print("\nCalculation of worksite by points with space resection.\n")
    work = space_resection_on_points_to_shot()
    for name_shot, shot in work.shots.items():
        print(f"Shot {name_shot} are position: {shot.pos_shot} and orientation {shot.ori_shot}")


"""
####### detail letter in header file point ########

S: to ignore the column
P: name of point
N: name of shot
T: Type of gcp to control.
X: coordinate x (column) in the image
Y: coordinate y (line) in the image
X: coordinate x of the shot position
Y: coordinate y of the shot position
Z: coordinate z of the shot position
"""
