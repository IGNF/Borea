"""
Main to control opk file
"""
import argparse
from src.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk
from src.process.p_func.p_control import args_control, process_args_control


parser = argparse.ArgumentParser(description='Photogrammetric site control opk file')

# Args for implement control opk
parser = args_reading_opk(parser)
parser = args_control(parser)

args = parser.parse_args()

# Process to read data
work = process_args_read_opk(args)
# Process to control data
process_args_control(args, work)