"""
Main to convert opk file to an light conical file (it's an xml file for GEOVIEW IGN France)
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk  # noqa: E402
from borea.process.p_format.p_write_con import args_write_con, process_args_write_con  # noqa: E402


def opk_to_conl():
    """
    Converts an OPK file into an light conical (IGN format) file.
    """
    parser = argparse.ArgumentParser(description='Photogrammetric site conversion '
                                                 'opk to conical file.')
    # Args for implement opk to conl
    parser = args_reading_opk(parser)
    parser = args_write_con(parser)

    args = parser.parse_args()

    # Process to read data
    work = process_args_read_opk(args)
    # Process to write conl
    process_args_write_con(args, work)


if __name__ == "__main__":
    opk_to_conl()
