"""
Main to calculate image coodinate of the ground point.
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_add_data.p_add_shot import args_add_shot, process_add_shot  # noqa: E402
from borea.process.p_add_data.p_pt2d import args_add_pt2d, process_image_world  # noqa: E402


def pt_image_to_world():
    """
    Converts a image point into an terrain point.
    """
    parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
    # Args for implement pt image to world
    parser = args_add_shot(parser)
    parser = args_add_pt2d(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_add_shot(args)
    # Process to transform image to world
    process_image_world(args, work)


if __name__ == "__main__":
    pt_image_to_world()
