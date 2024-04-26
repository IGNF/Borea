"""
Main to calculate 6 externals parameters of shots and save in opk file.
"""
# pylint: disable=import-error, wrong-import-position, line-too-long
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_func.p_spaceresection import args_space_resection, process_space_resection  # noqa: E402, E501
from borea.process.p_format.p_write_opk import args_writing_opk, process_args_write_opk  # noqa: E402


parser = argparse.ArgumentParser(description='Space resection of point file image and world'
                                             ' to calculate 6 externals parameters of shots')
# Args for implement space resection( opk
parser = args_space_resection(parser)
parser = args_writing_opk(parser)

args = parser.parse_args()

# Process to read data
work = process_space_resection(args)
# Process to space resection
process_args_write_opk(args, work)
