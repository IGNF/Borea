"""
Args of parser to control file
"""
import argparse
from borea.worksite.worksite import Worksite
from borea.process.p_add_data.p_file_gcp2d import args_gcp2d, process_gcp2d
from borea.process.p_add_data.p_file_gcp3d import args_gcp3d, process_gcp3d
from borea.stat.statistics import Stat
from borea.transform_world_image.transform_worksite.world_image_work import WorldImageWork
from borea.transform_world_image.transform_worksite.image_world_work import ImageWorldWork


def args_control(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_gcp2d(parser)
    parser = args_gcp3d(parser)
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


def process_args_control(args, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Read GCP 2D
    work = process_gcp2d(args, work)

    # Read GCP 3D
    work = process_gcp3d(args, work)

    # Calculate ground coordinate of conneting point by intersection
    print("Calculation of data image to world.")
    ImageWorldWork(work).manage_image_world(type_point="gcp2d",
                                            type_process=args.process,
                                            control_type=args.control_type)

    # Calculate image coordinate of GCP if they exist
    print("Calculation of data world to image.")
    WorldImageWork(work).calculate_world_to_image(args.control_type)

    # Statistics
    print("Make statistics.")
    stat = Stat(work, args.pathreturn, args.control_type)
    stat.main_stat_and_save()
    print("Statistics on control point, if there are,")
    print(f" in {args.pathreturn}Stat_module_{work.name}.txt .")
