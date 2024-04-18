"""
Main to calculate image coodinate with opk.
"""
import argparse
from src.process.p_format.p_read_opk import args_reading_opk, process_args_read_opk
from src.process.p_func.p_world_image import args_world_image, process_world_image


parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
# Args for implement ptfile world to image
parser = args_reading_opk(parser)
parser = args_world_image(parser)

args = parser.parse_args()

# Process to read data
work = process_args_read_opk(args)
# Process to transform world to image
process_world_image(args, work)
