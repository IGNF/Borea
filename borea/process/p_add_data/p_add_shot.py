"""
Args of parser for adding one shot
"""
import argparse
import numpy as np
from borea.process.p_add_data.p_gen_param import args_general_param, process_args_gen_param
from borea.process.p_add_data.p_unit_shot import args_input_shot
from borea.worksite.worksite import Worksite


def args_add_shot(parser: argparse) -> argparse:
    """
    Args for adding one shot.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-n', '--name_shot',
                        type=str, default='Test',
                        help='Name of the shot.')
    parser.add_argument('-s', '--pos_shot',
                        type=float, nargs=3,
                        help='Position of the shot X Y Z.')
    parser.add_argument('-t', '--unit_z_shot',
                        type=str, choices=['altitude', 'height'],
                        help='Unit of the z of the shot.')
    parser.add_argument('-o', '--ori_shot',
                        type=float, nargs=3,
                        help='Orientation of the shot Omega Phi Kappa.')
    parser = args_input_shot(parser)
    parser = args_general_param(parser)
    return parser


def process_add_shot(args: argparse) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data)

    Returns:
        Worksite: data
    """
    work = Worksite("Calc_one_img")
    work = process_args_gen_param(args, work)

    work.add_shot(args.name_shot,
                  np.array(args.pos_shot),
                  np.array(args.ori_shot),
                  work.cameras[list(work.cameras.keys())[0]].name_camera,
                  args.unit_angle,
                  args.linear_alteration,
                  args.order_axe_input)

    work.set_param_shot(args.approx_system)

    work.type_z_shot = args.unit_z_shot

    return work
