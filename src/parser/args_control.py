"""
Args of parser to control file
"""
import argparse
from src.worksite.worksite import Worksite
from src.reader.reader_ground_img_pts import read_ground_image_points
from src.reader.reader_gcp import read_gcp
from src.stat.statistics import Stat
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork


def args_control(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-t', '--gcp2d',
                        type=str, default=None,
                        help='File path of ground control points in images.')
    parser.add_argument('-g', '--gcp3d',
                        type=str, default=None,
                        help='File path of ground control points in ground.')
    parser.add_argument('-d', '--control_type',
                        type=int, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser.add_argument('--fg', '--format_gcp',
                        type=str, default=None, choices=["altitude", "height"],
                        help='Format of GCP and ground image point "altitude" or "height".')
    parser.add_argument('-p', '--process',
                        type=str, default="inter", choices=["inter", "square"],
                        help="Type of process for the function image to world,"
                             "intersection or least_square")
    parser.add_argument('-x', '--approx_system',
                        type=bool, default=False,
                        help="To use an approximate system.")
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
    # Reading ground point image
    if args.gcp2d is not None:
        read_ground_image_points(args.gcp2d, work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = args.fg
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("Connecting point reading done.")
        count = 0
        for k in work.ground_img_pts.values():
            count += len(k)
        print(f"Number of ground points of image: {len(work.ground_img_pts)}")
        print(f"Number of image with ground point.s: {count}")

    # Reading GCP
    if args.gcp3d is not None:
        read_gcp(args.gcp3d, work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = args.fg
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("GCP reading done.")
        print(f"Number of gcp: {len(work.gcps)}")

    # Calculate ground coordinate of conneting point by intersection
    ImageWorldWork(work).manage_image_world(type_point="ground_img_pts",
                                            type_process=args.process,
                                            control_type=args.control_type)

    # Calculate image coordinate of GCP if they exist
    WorldImageWork(work).calculate_world_to_image(args.control_type)

    # Statistics
    stat = Stat(work, args.pathreturn, args.control_type)
    stat.main_stat_and_save()
    print("Statistics on control point, if there are,")
    print(f" in {args.pathreturn}Stat_module_{work.name}.txt .")
