"""
Main to calculate world coodinate of the image point.
"""
import argparse
from src.process.p_add_data.p_add_shot import args_add_shot, process_add_shot
from src.process.p_add_data.p_pt3d import args_add_pt3d, process_world_image


parser = argparse.ArgumentParser(description='Calculate world coodinate of the image point.')
# Args for implement pt world to image
parser = args_add_shot(parser)
parser = args_add_pt3d(parser)

args = parser.parse_args()

# Process to read data
work = process_add_shot(args)
# Process to transform world to image
process_world_image(args, work)