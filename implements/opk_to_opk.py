"""
Main to convert opk file to an other opk file
"""
import argparse
from src.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk
from src.process.p_format.p_write_opk import args_writing_opk, process_args_write_opk


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
