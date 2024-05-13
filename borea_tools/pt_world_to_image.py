"""
Main to calculate world coodinate of the image point.
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_add_data.p_add_shot import args_add_shot, process_add_shot  # noqa: E402
from borea.process.p_add_data.p_pt3d import args_add_pt3d, process_world_image  # noqa: E402


def pt_world_to_image():
    """
    Converts a terrain point into an image point.
    """
    parser = argparse.ArgumentParser(description='Calculate world coodinate of the image point.')
    # Args for implement pt world to image
    parser = args_add_shot(parser)
    parser = args_add_pt3d(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_add_shot(args)
    # Process to transform world to image
    process_world_image(args, work)


if __name__ == "__main__":
    pt_world_to_image()
