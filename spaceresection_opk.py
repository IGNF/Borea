"""
Main to calculate 6 externals parameters of shots and save in opk file.
"""
import argparse

from src.parser.parser_func.args_spaceresection import args_space_resection, process_space_resection
from src.parser.parser_format.args_write_opk import args_writing_opk, process_args_write_opk


parser = argparse.ArgumentParser(description='Space resection of point file image and world'
                                             ' to calculate 6 externals parameters of shots')
parser = args_space_resection(parser)
parser = args_writing_opk(parser)

args = parser.parse_args()

work = process_space_resection(args)
process_args_write_opk(args, work)
