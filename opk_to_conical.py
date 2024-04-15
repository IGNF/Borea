"""
Main to convert opk file to an conical file (it's an xml file for GEOVIEW IGN France)
"""
import argparse
from src.parser.parser_format.args_read_opk import args_reading_opk, process_args_read_opk
from src.parser.parser_format.args_write_con import args_write_con, process_args_write_con


parser = argparse.ArgumentParser(description='Photogrammetric site conversion '
                                             'opk to conical file.')

parser = args_reading_opk(parser)
parser = args_write_con(parser)

args = parser.parse_args()

work = process_args_read_opk(args)
process_args_write_con(args, work)
