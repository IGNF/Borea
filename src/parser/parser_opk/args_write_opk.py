"""
Args of parser for writing opk file
"""
import argparse
from src.worksite.worksite import Worksite
from src.writer.manage_writer import manager_writer


def args_writing_opk(parser: argparse) -> argparse:
    """
    Args for writing opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    # pylint: disable=duplicate-code
    parser.add_argument('-n', '--name',
                        type=str,
                        help='Name of the new file.')
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    parser.add_argument('-o', '--output_header',
                        type=str,
                        help='Type of each column in the site file.'
                        'e.g. "N X Y Z O P K C"'
                        'N: name of shot'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position in altitude'
                        'H: coordinate z of the shot position in height'
                        'O: omega rotation angle'
                        'P: phi rotation angle'
                        'K: kappa rotation angle'
                        'C: name of the camera')
    parser.add_argument('-d', '--output_unit_angle',
                        type=str, default="degree", choices=["degree", "radian"],
                        help="Unit of the angle of shooting, 'degree' or 'radian'")
    parser.add_argument('-l', '--output_linear_alteration',
                        type=bool, default=True,
                        help="True if z shot corrected by linear alteration.")
    return parser


def process_args_write_opk(args: argparse, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Writing data
    if args.name is not None:
        if args.output_header is not None:
            args_writing = {"header": args.output_header,
                            "unit_angle": args.output_unit_angle,
                            "linear_alteration": args.output_linear_alteration}
            manager_writer("opk", args.name, args.pathreturn, args_writing, work)
            print(f"File written in {args.pathreturn + args.name}.opk.")
        else:
            raise ValueError("The output header file is missing -o.")
    else:
        raise ValueError("The name of the saving file is missing -n.")
