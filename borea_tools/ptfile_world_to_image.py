"""
Main to calculate image coodinate with opk.
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk  # noqa: E402
from borea.process.p_func.p_world_image import args_world_image, process_world_image  # noqa: E402


def ptfile_world_to_image():
    """
    Converts a terrain point file into an image point file.
    """
    parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
    # Args for implement ptfile world to image
    parser = args_reading_opk(parser)
    parser = args_world_image(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_args_read_opk(args)
    # Process to transform world to image
    process_world_image(args, work)


if __name__ == "__main__":
    ptfile_world_to_image()
