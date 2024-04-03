"""
Args of parser to control file
"""
import argparse
from src.worksite.worksite import Worksite
from src.reader.reader_point import read_file_pt
from src.stat.statistics import Stat
from src.transform_world_image.transform_worksite.world_image_work import WorldImageWork
from src.transform_world_image.transform_worksite.image_world_work import ImageWorldWork


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
    parser.add_argument('-k', '--head_gcp2d',
                        type=str, default="PNXY",
                        help='Header of the file gcp2d.'
                        'e.g. PNXY'
                        'S: to ignore the column'
                        'P: name of point'
                        'N: name of shot'
                        'X: coordinate x (column) in the image'
                        'Y: coordinate y (column) in the image')
    parser.add_argument('-g', '--gcp3d',
                        type=str, default=None,
                        help='File path of ground control points in ground.')
    parser.add_argument('-l', '--head_gcp3d',
                        type=str, default="PTXYZ",
                        help='Header of the file gcp2d.'
                        'e.g. PTXYZ'
                        'S: to ignore the column'
                        'P: name of point'
                        'T: Type of gcp to control.'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position')
    parser.add_argument('-d', '--control_type',
                        type=str, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser.add_argument('--fg', '--format_gcp',
                        type=str, default=None, choices=["altitude", "height"],
                        help='Format of GCP and ground image point "altitude" or "height".')
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
    # Reading ground point image
    if args.gcp2d is not None:
        read_file_pt(args.gcp2d, list(args.head_gcp2d.upper()), "gcp2d", work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = args.fg
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("Connecting point reading done.")
        count = 0
        for k in work.gcp2d.values():
            count += len(k)
        print(f"Number of gcp 2D in image: {len(work.gcp2d)}")
        print(f"Number of image with gcp 2D: {count}")

    # Reading GCP
    if args.gcp3d is not None:
        read_file_pt(args.gcp3d, list(args.head_gcp3d.upper()), "gcp3d", work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = args.fg
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("GCP reading done.")
        print(f"Number of gcp: {len(work.gcp3d)}")

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
