"""
Args of parser to calcule world coordinate.
"""
import argparse
from src.worksite.worksite import Worksite
from src.parser.parser_adata.args_file_gcp2d import args_gcp2d, process_gcp2d
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork


def args_image_world(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_gcp2d(parser)
    parser.add_argument('-d', '--control_type',
                        type=str, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser.add_argument('-p', '--process',
                        type=str, default="inter", choices=["inter", "square"],
                        help="Type of process for the function image to world,"
                             "intersection or least_square")
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    return parser


def process_image_world(args, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Read GCP 2D
    work = process_gcp2d(args, work)

    # Calculate ground coordinate of conneting point by intersection
    print("Calculation of data image to world.")
    ImageWorldWork(work).manage_image_world(type_point="gcp2d",
                                            type_process=args.process,
                                            control_type=args.control_type)
