"""
Main to calculate image coodinate of the ground point.
"""
import argparse
from src.parser.parser_func.args_add_shot import args_add_shot, process_add_shot
from src.parser.parser_func.args_pt2d import args_add_pt2d, process_image_world


parser = argparse.ArgumentParser(description='Calculate image coodinate of the ground point.')
parser = args_add_shot(parser)
parser = args_add_pt2d(parser)

args = parser.parse_args()

work = process_add_shot(args)
process_image_world(args, work)
