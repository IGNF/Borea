"""
Main to calculate world coodinate with opk.
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk  # noqa: E402
from src.process.p_func.p_image_world import args_image_world, process_image_world  # noqa: E402


parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
# Args for implement ptfile image to world
parser = args_reading_opk(parser)
parser = args_image_world(parser)

args = parser.parse_args()

# Process to read data
work = process_args_read_opk(args)
# Process to transform image to world
process_image_world(args, work)
