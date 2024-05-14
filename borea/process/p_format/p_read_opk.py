"""
Args of parser for reading opk file
"""
import argparse
from borea.process.p_add_data.p_gen_param import args_general_param, process_args_gen_param
from borea.process.p_add_data.p_unit_shot import args_input_shot
from borea.worksite.worksite import Worksite
from borea.reader.orientation.manage_reader import reader_orientation


def args_reading_opk(parser: argparse) -> argparse:
    """
    Args for reading opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    # pylint: disable=duplicate-code
    parser.add_argument('-r', '--filepath',
                        type=str, help='File path of the workfile.')
    parser.add_argument('-i', '--header',
                        type=str, default="NXYZOPKC",
                        help='Type of each column in the site file.'
                        'e.g. NXYZOPKC'
                        'S: to ignore the column'
                        'N: name of shot'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position in altitude'
                        'H: coordinate z of the shot position in height'
                        'O: omega rotation angle'
                        'P: phi rotation angle'
                        'K: kappa rotation angle'
                        'C: name of the camera')
    parser.add_argument('-f', '--first_line',
                        type=int, default=1,
                        help='Line number to start file playback. First line in the file is 1.'
                             ' Does not take file header into account.')
    parser.add_argument('-z', '--last_line',
                        type=int, default=None,
                        help='Line number to end file playback.'
                             ' If not set, all lines below -f will be read.')
    parser = args_input_shot(parser)
    parser = args_general_param(parser)
    return parser


def process_args_read_opk(args: argparse) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data)

    Returns:
        Worksite: data
    """
    # Readind data
    if args.filepath is not None:
        if args.header is not None:
            work = reader_orientation(args.filepath, {"order_axe": args.order_axe_input.lower(),
                                                      "interval": [args.first_line, args.last_line],
                                                      "header": list(args.header.upper()),
                                                      "unit_angle": args.unit_angle,
                                                      "linear_alteration": args.linear_alteration})
            print("Orientation file reading done.")
            print(f"Number of image: {len(work.shots)}")
        else:
            raise ValueError("The header file is missing -i.")
    else:
        raise ValueError("The access road to the photogrammetric site is missing -r.")

    work = process_args_gen_param(args, work)

    return work
