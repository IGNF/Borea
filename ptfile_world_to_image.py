"""
Main to calculate image coodinate with opk.
"""
import argparse
from src.parser.parser_opk.args_read_opk import args_reading_opk, process_args_read_opk
from src.parser.parser_func.args_world_image import args_world_image, process_world_image


parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
parser = args_reading_opk(parser)
parser = args_world_image(parser)

args = parser.parse_args()

work = process_args_read_opk(args)
process_world_image(args, work)
