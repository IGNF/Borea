"""
Args of parser for reading opk file
"""
import argparse
from src.worksite.worksite import Worksite
from src.reader.reader_camera import read_camera
from src.reader.orientation.manage_reader import reader_orientation


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
                        type=str,
                        help='Type of each column in the site file.'
                        'e.g. "N X Y Z O P K C"'
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
    parser.add_argument('-u', '--unit_angle',
                        type=str, default="degree",
                        help="Unit of the angle of shooting, 'degree' or 'radian'")
    parser.add_argument('-a', '--linear_alteration',
                        type=bool, default=True,
                        help="True if z shot corrected by linear alteration.")
    parser.add_argument('-f', '--first_line',
                        type=int, default=None,
                        help='Line number to start file playback.'
                             ' Does not take file header into account.')
    parser.add_argument('-z', '--last_line',
                        type=int, default=None,
                        help='Line number to end file playback.'
                             ' If not set, all lines below -l will be read.')
    parser.add_argument('-e', '--epsg',
                        type=int, default=None,
                        help='EPSG codifier number of the reference system used e.g. "2154".')
    parser.add_argument('-j', '--pathepsg',
                        type=str, default=None,
                        help='Path to the json file which list the code epsg, you use.')
    parser.add_argument('-y', '--pathgeotiff',
                        type=str, default=None,
                        help='Path to the folder which contains pyproj GeoTIFF of the geoid '
                             'e.g../test/data/ or they must be in usr/share/proj or '
                             'env_name/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.')
    parser.add_argument('-c', '--camera',
                        type=str, nargs='*',
                        help='Files paths of cameras (xml or txt).')
    parser.add_argument('-m', '--dtm',
                        type=str, default=None,
                        help='DtM of the worksite.')
    parser.add_argument('--fm', '--format_dtm',
                        type=str, default=None,
                        help='Format of Dtm "altitude" or "height".')
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
            work = reader_orientation(args.filepath, {"interval": [args.first_line, args.last_line],
                                                      "header": args.header,
                                                      "unit_angle": args.unit_angle,
                                                      "linear_alteration": args.linear_alteration})
            print("Orientation file reading done.")
            print(f"Number of image: {len(work.shots)}")
        else:
            raise ValueError("The header file is missing -i.")
    else:
        raise ValueError("The access road to the photogrammetric site is missing -r.")

    # Add a projection to the worksite
    if args.epsg is not None:
        work.set_proj(args.epsg, args.pathepsg, args.pathgeotiff)
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

    return work
