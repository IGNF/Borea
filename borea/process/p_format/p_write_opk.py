"""
Args of parser for writing opk file
"""
import argparse
from borea.process.p_add_data.p_unit_shot import args_output_shot
from borea.process.p_add_data.p_write import args_writer
from borea.worksite.worksite import Worksite
from borea.writer.manage_writer import manager_writer


def args_writing_opk(parser: argparse) -> argparse:
    """
    Args for writing opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    # pylint: disable=duplicate-code
    parser = args_writer(parser)
    parser.add_argument('-o', '--output_header',
                        type=str, default=None,
                        help='Type of each column in the site file.'
                        'e.g. NXYZOPKC'
                        'N: name of shot'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position in altitude'
                        'H: coordinate z of the shot position in height'
                        'O: omega rotation angle'
                        'P: phi rotation angle'
                        'K: kappa rotation angle'
                        'C: name of the camera')
    parser = args_output_shot(parser)
    return parser


def process_args_write_opk(args: argparse, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    if args.order_axe_output:
        args.order_axe_output = args.order_axe_output.lower()

    if args.output_header:
        args.output_header = list(args.output_header.upper())

    # Writing data
    print("Writing OPK.")
    if args.namereturn is not None:
        args_writing = {"order_axe": args.order_axe_output,
                        "header": args.output_header,
                        "unit_angle": args.output_unit_angle,
                        "linear_alteration": args.output_linear_alteration}
        manager_writer("opk", args.namereturn, args.pathreturn, args_writing, work)
        print(f"File written in {args.pathreturn + args.namereturn}.opk.")
    else:
        raise ValueError("The name of the saving file is missing -n.")
