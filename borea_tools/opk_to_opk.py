"""
Main to convert opk file to an other opk file
"""
# pylint: disable=import-error, wrong-import-position, line-too-long
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk  # noqa: E402
from borea.process.p_format.p_write_opk import args_writing_opk, process_args_write_opk  # noqa: E402, E501


def opk_to_opk():
    """
    Converts an OPK file into an OPK file.
    """
    parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                                 ' and manipulation software opk to opk.')
    # Args for implement opk to opk
    parser = args_reading_opk(parser)
    parser = args_writing_opk(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_args_read_opk(args)
    # Process to write opk
    process_args_write_opk(args, work)


if __name__ == "__main__":
    opk_to_opk()
