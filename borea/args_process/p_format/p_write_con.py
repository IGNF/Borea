"""
Args of parser for writing conical file
"""
import argparse
from borea.worksite.worksite import Worksite
from borea.writer.manage_writer import manager_writer


def args_write_con(parser: argparse) -> argparse:
    """
    Args for writing conical file of GEOVIEW IGN.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    return parser


def process_args_write_con(args: argparse, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Writing data
    print("Writing Conical file.")
    manager_writer("con", None, args.pathreturn, None, work)
    print(f"File written in folder {args.pathreturn} in .CON format.")
