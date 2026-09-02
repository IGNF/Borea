"""
Main to control opk file
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_format.p_read_file import args_reading, process_args_read  # noqa: E402
from borea.process.p_func.p_control import args_control, process_args_control  # noqa: E402


def opk_control():
    """
    Controls the accuracy of an OPK file with support points.
    """
    parser = argparse.ArgumentParser(description='Photogrammetric site control opk file')

    # Args for implement control opk
    parser = args_reading(parser)
    parser = args_control(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_args_read(args)
    # Process to control data
    process_args_control(args, work)


if __name__ == "__main__":
    opk_control()
