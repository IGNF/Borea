"""
Main to calculate world coodinate of the image point.
"""
import argparse
from src.parser.parser_func.args_add_shot import args_add_shot, process_add_shot
from src.parser.parser_func.args_pt3d import args_add_pt3d, process_world_image


parser = argparse.ArgumentParser(description='Calculate world coodinate of the image point.')
parser = args_add_shot(parser)
parser = args_add_pt3d(parser)

args = parser.parse_args()

work = process_add_shot(args)
process_world_image(args, work)
