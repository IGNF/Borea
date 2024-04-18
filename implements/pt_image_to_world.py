"""
Main to calculate image coodinate of the ground point.
"""
import argparse
from src.process.p_add_data.p_add_shot import args_add_shot, process_add_shot
from src.process.p_add_data.p_pt2d import args_add_pt2d, process_image_world


parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
# Args for implement pt image to world
parser = args_add_shot(parser)
parser = args_add_pt2d(parser)

args = parser.parse_args()

# Process to read data
work = process_add_shot(args)
# Process to transform image to world
process_image_world(args, work)
