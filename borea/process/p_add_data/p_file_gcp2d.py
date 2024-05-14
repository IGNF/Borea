"""
Args of parser to read gcp 2D file.
"""
import argparse
from borea.worksite.worksite import Worksite
from borea.reader.reader_point import read_file_pt


def args_gcp2d(parser: argparse) -> argparse:
    """
    Args to read gcp 2D file.

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
                        'Y: coordinate y (line) in the image')
    return parser


def process_gcp2d(args, work: Worksite) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.

    Returns:
        Worksite: data
    """
    # Reading ground point image
    if args.gcp2d is not None:
        read_file_pt(args.gcp2d, list(args.head_gcp2d.upper()), "gcp2d", work)
        print("Connecting point reading done.")
        count = 0
        for k in work.gcp2d.values():
            count += len(k)
        print(f"Number of gcp 2D in image: {len(work.gcp2d)}")
        print(f"Number of image with gcp 2D: {count}")

    return work
