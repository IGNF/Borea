"""
Main to calculate world coodinate with opk.
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk  # noqa: E402
from borea.process.p_func.p_image_world import args_image_world, process_image_world  # noqa: E402


def ptfile_image_to_world():
    """
    Converts a image point file into an terrain point file.
    """
    parser = argparse.ArgumentParser(description='Calculate ground coodinate of the image point.')
    # Args for implement ptfile image to world
    parser = args_reading_opk(parser)
    parser = args_image_world(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_args_read_opk(args)
    # Process to transform image to world
    process_image_world(args, work)


if __name__ == "__main__":
    ptfile_image_to_world()
