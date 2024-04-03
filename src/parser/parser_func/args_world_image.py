"""
Args of parser to calcule image coordinate.
"""
import argparse
from src.worksite.worksite import Worksite
from src.parser.parser_adata.args_file_gcp3d import args_gcp3d, process_gcp3d
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork


def args_control(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_gcp3d(parser)
    parser.add_argument('-d', '--control_type',
                        type=str, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    return parser


def process_args_control(args, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Read GCP 3D
    work = process_gcp3d(args, work)

    # Calculate image coordinate of GCP if they exist
    print("Calculation of data world to image.")
    WorldImageWork(work).calculate_world_to_image(args.control_type)
