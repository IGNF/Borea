"""
Main to control opk file
"""
import argparse
from src.parser.parser_format.args_read_opk import args_reading_opk, process_args_read_opk
from src.parser.parser_func.args_control import args_control, process_args_control


parser = argparse.ArgumentParser(description='Photogrammetric site control opk file')
parser = args_reading_opk(parser)
parser = args_control(parser)

args = parser.parse_args()

work = process_args_read_opk(args)
process_args_control(args, work)
