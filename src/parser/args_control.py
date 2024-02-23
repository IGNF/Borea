"""
Args of parser to control file
"""
import argparse
from src.datastruct.worksite import Worksite
from src.reader.reader_ground_img_pts import read_ground_image_points
from src.reader.reader_gcp import read_gcp
from src.stat.statistics import Stat


def args_control(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file

    Args:
        parser (argparse): parser to add argument

    Returns:
        argsparse: parser with argument
    """
    parser.add_argument('-t', '--ground_points',
                        type=str, default=None, nargs='*',
                        help='Files paths of ground points in images (.mes).')
    parser.add_argument('-g', '--gcp',
                        type=str, default=None, nargs='*',
                        help='Files paths of GCP (.app).')
    parser.add_argument('-d', '--control_type',
                        type=int, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser.add_argument('--fg', '--format_gcp',
                        type=str, default=None,
                        help='Format of GCP and ground image point "altitude" or "height".')
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    return parser


def process_args_control(args, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): arg to apply on worksite (data)
        work (Worksite): data
    """
    # Reading ground point image
    if args.ground_points is not None:
        read_ground_image_points(args.ground_points, work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = "h" if args.fg == "height" else "a"
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("Connecting point reading done.")
        count = 0
        for k in work.gipoints.values():
            count += len(k)
        print(f"Number of ground points of image: {len(work.gipoints)}")
        print(f"Number of image with ground point.s: {count}")

    # Reading GCP
    if args.gcp is not None:
        read_gcp(args.gcp, work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = "h" if args.fg == "height" else "a"
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("GCP reading done.")
        print(f"Number of gcp: {len(work.gcps)}")

    # Calculate ground coordinate of conneting point by intersection

    # Calculate image coordinate of GCP if they exist
    work.calculate_world_to_image_gcp(args.control_type)

    # Statistics
    stat = Stat(work, args.pathreturn, args.control_type)
    stat.main_stat_and_save()
    print("Statistics on control point, if there are,")
    print(f" in {args.pathreturn}Stat_module_{work.name}.txt .")
