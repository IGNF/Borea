"""
Args of parser to calcule 6 externals parameters of shots.
"""
import argparse

import numpy as np
from src.parser.parser_adata.args_file_gcp2d import args_gcp2d
from src.parser.parser_adata.args_gen_param import args_general_param, process_args_gen_param
from src.parser.parser_adata.args_pt3d import args_add_pt3d
from src.reader.reader_point import read_file_pt_dataframe
from src.transform_world_image.transform_worksite.space_resection import SpaceResection
from src.utils.check.check_args_opk import check_header_file
from src.worksite.worksite import Worksite
from src.parser.parser_adata.args_file_gcp3d import args_gcp3d


def args_space_resection(parser: argparse) -> argparse:
    """
    Args to calcule 6 externals parameters of shots.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_add_pt3d(parser)
    parser = args_general_param(parser)
    parser = args_gcp2d(parser)
    parser = args_gcp3d(parser)
    return parser


def process_space_resection(args: argparse) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).

    Returns:
        Worksite: data
    """
    work = Worksite("Space_Resection")
    work = process_args_gen_param(args, work)
    work.set_type_z_shot(check_header_file(list(args.output_header.upper()))[1])
    work.set_type_z_data(args.fg)
    pt2d = read_file_pt_dataframe(args.gcp2d, args.head_gcp2d, "pt2d")
    pt3d = read_file_pt_dataframe(args.gcp3d, args.head_gcp3d, "pt3d")
    pinit = {"coor_init": np.array(args.point3d)}
    SpaceResection(work).space_resection_to_worksite(pt2d, pt3d, pinit)
    return work
