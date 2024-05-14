"""
Example to use opk control in lib python (main line 45)
"""
# pylint: disable=import-error, missing-function-docstring
# pylint: disable=wrong-import-position, pointless-string-statement
import sys
import os
from eg_build_worksite_by_file import worksite_add_gcp2d, worksite_add_gcp3d, worksite_opk

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.stat.statistics import Stat  # noqa: E402
# pylint: disable-next=line-too-long
from borea.transform_world_image.transform_worksite.image_world_work import ImageWorldWork  # noqa: E402, E501
# pylint: disable-next=line-too-long
from borea.transform_world_image.transform_worksite.world_image_work import WorldImageWork  # noqa: E402, E501


OUTPUT_PATH = "./test/tmp"


def opk_control(pathreturn: str, type_control: list) -> None:
    """
    The Stat().main_stat_and_save() function produces statistics on the results
    of world-to-image and image-to-world transformations on gcp.
    You must therefore perform the transformations before using the Stat class,
    otherwise no n,i result file will be created.
    """
    # Build Worksite
    work = worksite_opk()

    # Add ground control point image (gcp2d)
    work = worksite_add_gcp2d(work)

    # Add ground control point terrain (gcp3d)
    work = worksite_add_gcp3d(work)

    # Make transformation image to world and world to image of gcp
    WorldImageWork(work).calculate_world_to_image(type_control)
    ImageWorldWork(work).manage_image_world(type_point="gcp2d")

    # Calculate stat on world_to_image and image_to_world
    Stat(work, pathreturn, type_control).main_stat_and_save()


if __name__ == "__main__":
    ############################################
    #   Statistics to control position of opk  #
    ############################################
    # You need path of folder where you want to save statistics file OUTPUT_PATH

    # Creation of folder
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # You need the control type of gcp
    # control_type = [13]  # Take just gcp with type 13
    control_type = []  # Take all gcp of any type

    print(f"\nControl OPK with statistics file in {OUTPUT_PATH}")
    opk_control(OUTPUT_PATH, control_type)

    """
    OUTPUT OF THE FUNCTION

    There are 4 output files:
    - 2 metrics files:
        - image to world metric (Stat_metric_image_to_world_{name_opk}.txt)
        - world to image metric (Stat_metric_world_to_image_{name_opk}.txt)
    Give Min, Max, Median, Mean, Var and Sigam ain arthmetic and absolut
    of residu of transformation coordinates point.

    - 2 residus files
        - image to world residu (Stat_residu_image_to_world_{name_opk}.txt)
        - world to image residu (Stat_residu_world_to_image_{name_opk}.txt)
    Give resudi in x, y, z or column, line of gcp
    """
