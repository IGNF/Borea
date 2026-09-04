"""
Args of parser to write file.
"""
import argparse

from borea.args_process.p_add_data.p_unit_shot import args_output_shot
from borea.worksite.worksite import Worksite
from borea.writer.manage_writer import manager_writer


def args_writer(parser: argparse) -> argparse:
    """
    Args to write file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-n', '--namereturn',
                        type=str, required=True,
                        help='Name of the new file.')
    parser = args_pathreturn(parser)
    return parser


def args_pathreturn(parser: argparse) -> argparse:
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


def process_args_write(args: argparse, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    if args.ob:
        args.ob = args.ob.lower()

    if args.output_header:
        args.output_header = list(args.output_header.upper())

    # Writing data
    print("Writing OPK.")
    if args.namereturn is not None:
        args_writing = {"order_axe": args.ob,
                        "header": args.output_header,
                        "unit_angle": args.ou,
                        "linear_alteration": args.oa}
        manager_writer("opk", args.namereturn, args.pathreturn, args_writing, work)
        print(f"File written in {args.pathreturn + args.namereturn}.opk.")
    else:
        raise ValueError("The name of the saving file is missing -n.")





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
