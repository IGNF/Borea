"""
Main to convert opk file to an conical file (it's an xml file for GEOVIEW IGN France)
"""
import argparse
from src.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk
from src.process.p_format.p_write_con import args_write_con, process_args_write_con


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
