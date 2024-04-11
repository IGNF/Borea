"""
Main to convert opk file to Rpc
"""
import argparse
from src.parser.parser_format.args_read_opk import args_reading_opk, process_args_read_opk
from src.parser.parser_format.args_write_rpc import args_writing_rpc, process_args_write_rpc


parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                             ' and manipulation software opk to rpc.')
parser = args_reading_opk(parser)
parser = args_writing_rpc(parser)

args = parser.parse_args()

work = process_args_read_opk(args)
process_args_write_rpc(args, work)
