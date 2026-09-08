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
    parser.add_argument('-n', '--name_return',
                        type=str, required=True,
                        help='Name of the new file.')
    parser = args_path_return(parser)
    return parser


def args_path_return(parser: argparse) -> argparse:
    """
    Args for writing conical file of GEOVIEW IGN.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-w', '--path_return',
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
    if args.name_return is not None:
        args_writing = {"order_axe": args.ob,
                        "header": args.output_header,
                        "unit_angle": args.ou,
                        "linear_alteration": args.oa}
        manager_writer("opk", args.name_return, args.path_return, args_writing, work)
        print(f"File written in {args.path_return + args.name_return}.opk.")
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
    manager_writer("con", None, args.path_return, None, work)
    print(f"File written in folder {args.path_return} in .CON format.")


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
    manager_writer("rpc", None, args.path_return, args_writing, work)
    print(f"File written in folder {args.path_return} .txt.")
