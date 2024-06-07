"""
Args of parser to calcule 6 externals parameters of shots.
"""
import argparse

import numpy as np
from borea.process.p_add_data.p_file_gcp2d import args_gcp2d
from borea.process.p_add_data.p_gen_param import args_general_param, process_args_gen_param
from borea.process.p_add_data.p_pt3d import args_add_pt3d
from borea.reader.reader_point import read_file_pt_dataframe
from borea.transform_world_image.transform_worksite.space_resection import SpaceResection
from borea.utils.check.check_args_opk import check_header_file
from borea.worksite.worksite import Worksite
from borea.process.p_add_data.p_file_gcp3d import args_gcp3d


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
    pt2d = read_file_pt_dataframe(args.gcp2d, list(args.head_gcp2d.upper()), "pt2d")
    pt3d = read_file_pt_dataframe(args.gcp3d, list(args.head_gcp3d.upper()), "pt3d")
    pinit = {"coor_init": np.array(args.point3d)}
    SpaceResection(work).space_resection_to_worksite(pt2d, pt3d, pinit)
    return work
