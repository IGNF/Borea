"""
Args of parser for writing Rpc file
"""
import argparse
from borea.worksite.worksite import Worksite
from borea.writer.manage_writer import manager_writer


def args_writing_rpc(parser: argparse) -> argparse:
    """
    Args for writing rpc file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    parser.add_argument('-o', '--order',
                        type=int, default=3, choices=[1, 2, 3],
                        help="Degree of the polynomial of the rpc (1, 2, 3)")
    parser.add_argument('-d', '--size_grid',
                        type=int, default=100,
                        help="Size of the grid to calculate Rpc.")
    parser.add_argument('-l', '--fact_rpc',
                        type=float, default=None,
                        help="Factor Rpc for pyproj convertion.")
    return parser


def process_args_write_rpc(args: argparse, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Writing data
    print("Writing Rpc.")
    args_writing = {"order": args.order,
                    "size_grid": args.size_grid,
                    "fact_rpc": args.fact_rpc}
    manager_writer("rpc", None, args.pathreturn, args_writing, work)
    print(f"File written in folder {args.pathreturn} .txt.")
