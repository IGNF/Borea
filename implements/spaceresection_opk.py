"""
Main to calculate 6 externals parameters of shots and save in opk file.
"""
import argparse
from src.process.p_func.p_spaceresection import args_space_resection, process_space_resection
from src.process.p_format.p_write_opk import args_writing_opk, process_args_write_opk


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
