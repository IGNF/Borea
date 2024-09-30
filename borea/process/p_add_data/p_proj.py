"""
Args of parser for reading projection parameters
"""
import argparse
import pyproj
from borea.worksite.worksite import Worksite


def args_proj_param(parser: argparse) -> argparse:
    """
    Args for adding projection parameter.

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
    parser.add_argument('--geog', '--epsg_geographic',
                        type=int, default=None,
                        help='EPSG codifier number of the reference geographic system.')
    parser.add_argument('--geoc', '--epsg_geocentric',
                        type=int, default=None,
                        help='EPSG codifier number of the reference geocentric system.')
    parser.add_argument('--oe', '--epsg_output',
                        type=int, default=None,
                        help="Code epsg of output Data")
    return parser


def process_args_proj_param(args: argparse, work: Worksite) -> Worksite:
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
        work.set_proj([args.epsg, args.geog, args.geoc], args.pathgeoid, args.oe)
        print(f"Projection set-up with EPSG:{args.epsg}.")
    else:
        print("There is no given projection.")

    return work
