"""
Args of parser to read gcp 3D file.
"""
import argparse
from borea.worksite.worksite import Worksite
from borea.reader.reader_point import read_file_pt


def args_gcp3d(parser: argparse) -> argparse:
    """
    Args to read gcp 3D file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-g', '--gcp3d',
                        type=str, default=None,
                        help='File path of ground control points in ground.')
    parser.add_argument('-l', '--head_gcp3d',
                        type=str, default="PTXYZ",
                        help='Header of the file gcp3d.'
                        'e.g. PTXYZ'
                        'S: to ignore the column'
                        'P: name of point'
                        'T: Type of gcp to control.'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position')
    parser.add_argument('--fg', '--format_gcp',
                        type=str, default=None, choices=["altitude", "height"],
                        help='Format of GCP and ground image point "altitude" or "height".')
    return parser


def process_gcp3d(args, work: Worksite) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.

    Returns:
        Worksite: data
    """
    # Reading GCP 3D
    if args.gcp3d is not None:
        read_file_pt(args.gcp3d, list(args.head_gcp3d.upper()), "gcp3d", work)
        if args.fg in ["altitude", "height"]:
            work.type_z_data = args.fg
        else:
            raise ValueError('Information on terrain point format is missing '
                             'or misspelled --fg altitude or height')
        print("GCP reading done.")
        print(f"Number of gcp: {len(work.gcp3d)}")

    return work
