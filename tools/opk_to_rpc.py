"""
Main to convert opk file to Rpc
"""
# pylint: disable=import-error, wrong-import-position
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk  # noqa: E402
from src.process.p_format.p_write_rpc import args_writing_rpc, process_args_write_rpc  # noqa: E402


parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                             ' and manipulation software opk to rpc.')
# Args for implement opk to rpc
parser = args_reading_opk(parser)
parser = args_writing_rpc(parser)

args = parser.parse_args()

# Process to read data
work = process_args_read_opk(args)
# Process to write rpc
process_args_write_rpc(args, work)
