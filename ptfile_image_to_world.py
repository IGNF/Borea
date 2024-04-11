"""
Main to calculate world coodinate with opk.
"""
import argparse
from src.parser.parser_format.args_read_opk import args_reading_opk, process_args_read_opk
from src.parser.parser_func.args_image_world import args_image_world, process_image_world


parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
parser = args_reading_opk(parser)
parser = args_image_world(parser)

args = parser.parse_args()

work = process_args_read_opk(args)
process_image_world(args, work)
