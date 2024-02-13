"""
pink lady launch module
"""
import argparse
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gipoints import read_gipoints
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_writer
from src.stat.statistics import Stat

parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                             ' and manipulation software.')
parser.add_argument('-w', '--filepath',
                    type=str, help='File path of the workfile.')
parser.add_argument('-i', '--header',
                    type=str, nargs='*',
                    help='Type of each column in the site file.'
                    'e.g. N X Y Zal Od Pd Kd C'
                    'S: to ignore the column'
                    'N: name of shot'
                    'X: coordinate x of the shot position'
                    'Y: coordinate y of the shot position'
                    'Z: coordinate z of the shot position'
                    'O: omega rotation angle'
                    'P: phi rotation angle'
                    'K: kappa rotation angle'
                    'C: name of the camera'
                    'Add unit for Z and angle.'
                    'h: height for Z'
                    'hl: height with linear alteration for Z'
                    'a: altitude for Z'
                    'al: altitude with linear alteration for Z'
                    'd: degrees for O P K'
                    'r: radian for O P K')
parser.add_argument('-f', '--first_line',
                    type=int, default=None,
                    help='Line number to start file playback.'
                         ' Does not take file header into account.')
parser.add_argument('-z', '--last_line',
                    type=int, default=None,
                    help='Line number to end file playback.'
                         ' If not set, all lines below -l will be read.')
parser.add_argument('-e', '--epsg',
                    type=str, default="2154",
                    help='EPSG codifier number of the reference system used e.g. "2154".')
parser.add_argument('-p', '--pathepsg',
                    type=str, default=None,
                    help='Path to the json file which list the code epsg, you use.')
parser.add_argument('-y', '--pathgeotiff',
                    type=str, default=None,
                    help='Path to the folder which contains pyproj GeoTIFF of the geoid '
                         'e.g../test/data/ or they must be in usr/share/proj or '
                         'env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj.')
parser.add_argument('-c', '--camera',
                    type=str, default=None, nargs='*',
                    help='Files paths of cameras (xml or txt).')
parser.add_argument('-l', '--connecting_points',
                    type=str, default=None, nargs='*',
                    help='Files paths of connecting points (.mes).')
parser.add_argument('-t', '--ground_points',
                    type=str, default=None, nargs='*',
                    help='Files paths of ground points in images (.mes).')
parser.add_argument('-g', '--gcp',
                    type=str, default=None, nargs='*',
                    help='Files paths of GCP (.app).')
parser.add_argument('-d', '--control_type',
                    type=int, default=[], nargs='*',
                    help='Type of gcp to control.')
parser.add_argument('--fg', '--format_gcp',
                    type=str, default=None,
                    help='Format of GCP and ground image point "altitude" or "height".')
parser.add_argument('-m', '--dem',
                    type=str, default=None,
                    help='DEM of the worksite.')
parser.add_argument('--fm', '--format_dem',
                    type=str, default=None,
                    help='Format of Dem "altitude" or "height".')
parser.add_argument('-o', '--writer',
                    type=str, default=None,
                    help='Worksite output file format e.g. opk.')
parser.add_argument('-r', '--pathreturn',
                    type=str, default='./',
                    help='Conversion path e.g. test/tmp/.')

args = parser.parse_args()

# Readind data
if args.filepath is not None:
    if args.header is not None:
        work = reader_orientation(args.filepath, [args.first_line, args.last_line], args.header)
        print("Orientation file reading done.")
        print(f"Number of image: {len(work.shots)}")
    else:
        raise ValueError("The header file is missing -i.")
else:
    raise ValueError("The access road to the photogrammetric site is missing -w.")

# Add a projection to the worksite
work.set_proj(args.epsg, args.pathepsg, args.pathgeotiff)
print(f"Projection set-up with EPSG:{args.epsg}.")

# Reading camera file
if args.camera is not None:
    read_camera(args.camera, work)
    print(f"Camera file reading done. {len(args.camera)} read")

# Reading connecting point
if args.connecting_points is not None:
    read_copoints(args.connecting_points, work)
    print("Connecting point reading done.")
    COUNT = 0
    for i, k in work.copoints.items():
        COUNT += len(k)
    print(f"Number of connecting points: {len(work.copoints)}")
    print(f"Number of image with connecting point.s: {COUNT}")

# Reading ground point image
if args.ground_points is not None:
    read_gipoints(args.ground_points, work)
    if args.fg in ["altitude", "height"]:
        work.type_z_data = "h" if args.fg == "height" else "a"
    else:
        raise ValueError('Information on terrain point format is missing '
                         'or misspelled --fg altitude or height')
    print("Connecting point reading done.")
    COUNT = 0
    for i, k in work.gipoints.items():
        COUNT += len(k)
    print(f"Number of ground points of image: {len(work.gipoints)}")
    print(f"Number of image with ground point.s: {COUNT}")

# Reading GCP
if args.gcp is not None:
    read_gcp(args.gcp, work)
    if args.fg in ["altitude", "height"]:
        work.type_z_data = "h" if args.fg == "height" else "a"
    else:
        raise ValueError('Information on terrain point format is missing '
                         'or misspelled --fg altitude or height')
    print("GCP reading done.")
    print(f"Number of gcp: {len(work.gcps)}")

# Add Dem
if args.dem is not None:
    work.add_dem(args.dem, args.fm)
    print("Add dem to the worksite done.")
else:
    print("Not Dem in the worksite.")

# Calculate ground coordinate of conneting point by intersection

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp(args.control_type)

# Statistics
stat = Stat(work, args.pathreturn, args.control_type)
stat.main_stat_and_save()
print("Statistics on control point, if there are,")
print(f" in {args.pathreturn}Stat_{work.name}.txt .")

# Writing data
if args.writer is not None:
    manager_writer(args.writer, args.pathreturn, work)
    print(f"File written in {args.pathreturn + work.name}.{args.writer} .")
