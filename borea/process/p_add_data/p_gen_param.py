"""
Args of parser for reading generals parameters
"""
import argparse
from borea.worksite.worksite import Worksite
from borea.process.p_add_data.p_proj import args_proj_param, process_args_proj_param
from borea.reader.reader_camera import read_camera


def args_general_param(parser: argparse) -> argparse:
    """
    Args for adding general parameter.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_proj_param(parser)
    parser.add_argument('-c', '--camera',
                        type=str, nargs='*',
                        help='Files paths of cameras (xml or txt).')
    parser.add_argument('-m', '--dtm',
                        type=str, default=None,
                        help='DtM of the worksite.')
    parser.add_argument('--fm', '--format_dtm',
                        type=str, default=None,
                        help='Format of Dtm "altitude" or "height".')
    parser.add_argument('-x', '--approx_system',
                        type=bool, default=False,
                        help="To use an approximate system.")
    return parser


def process_args_gen_param(args: argparse, work: Worksite) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Worksite to work on.

    Returns:
        Worksite: data
    """
    # Add a projection to the worksite
    work = process_args_proj_param(args, work)

    # Reading camera file
    if args.camera is not None:
        read_camera(args.camera, work)
        print(f"Camera file reading done. {len(args.camera)} read")
    else:
        print("There is no given camera.")

    # Add Dem
    work.set_dtm(args.dtm, args.fm)
    if args.dtm is not None:
        print("Add dtm to the worksite done.")
    else:
        print("Not Dtm in the worksite.")

    work.set_param_shot(args.approx_system)
    return work
