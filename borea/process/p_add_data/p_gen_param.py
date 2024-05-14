"""
Args of parser for reading generals parameters
"""
import argparse
import pyproj
from borea.worksite.worksite import Worksite
from borea.reader.reader_camera import read_camera


def args_general_param(parser: argparse) -> argparse:
    """
    Args for adding general parameter.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-e', '--epsg',
                        type=int, default=None,
                        help='EPSG codifier number of the reference system used e.g. "2154".')
    parser.add_argument('-y', '--pathgeoid',
                        type=str, nargs='*', default=None,
                        help='Path to the pyproj GeoTIFF of the geoid e.g../test/data/geoid.tif'
                             f' or they must be in {pyproj.datadir.get_data_dir()} and just'
                             ' need name of file e.g. geoid.tif.')
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
    if args.epsg is not None:
        work.set_proj(args.epsg, args.pathgeoid)
        print(f"Projection set-up with EPSG:{args.epsg}.")
    else:
        print("There is no given projection.")

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
