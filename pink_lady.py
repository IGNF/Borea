"""
pink lady launch module
"""
import sys
import argparse
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_writer

parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                             ' and manipulation software.')
parser.add_argument('-f', '--filepath',
                    type=str, default=None,
                    help='File path of the workfile (Nb arg 1).')
parser.add_argument('-skip', '--skip',
                    type=int, default=1,
                    help='Number of lines to be skipped before reading the file (Nb arg 1).')
parser.add_argument('-epsg', '--epsg',
                    type=str, default="EPSG:2154",
                    help='EPSG codifier number of the reference system used ex: "EPSG:2154"'
                    ' (Nb arg 1).')
parser.add_argument('-pepsg', '--pathepsg',
                    type=str, default=None,
                    help='Path to the json file which list the code epsg, you use (Nb arg 1).')
parser.add_argument('-ptif', '--pathgeotiff',
                    type=str, default=None,
                    help='Path to the folder which contains GeoTIFF ex:./test/data/ or '
                         'they must be in usr/share/proj or '
                         'env_name_folder/lib/python3.10/site-packages/pyproj/proj_dir/share/proj'
                         ' (Nb arg 1).')
parser.add_argument('-w', '--writer',
                    type=str, default=None,
                    help='Worksite output file format ex:opk (Nb arg 1).')
parser.add_argument('-pr', '--pathreturn',
                    type=str, default='test/tmp/',
                    help='Conversion path ex:test/tmp/ (Nb arg 1).')
parser.add_argument('-c', '--camera',
                    type=str, default=None, nargs='*',
                    help='Files paths of cameras (xml or txt) (Nb args [*]).')
parser.add_argument('-wh', '--widthxheight',
                    type=int, default=None, nargs=2,
                    help='Width and height of the camera (Nb args [width, height]).')
parser.add_argument('-cp', '--connecting_points',
                    type=str, default=None, nargs='*',
                    help='Files paths of connecting points (.mes) (Nb args [*]).')
parser.add_argument('-gcp', '--gcp',
                    type=str, default=None, nargs='*',
                    help='Files paths of GCP (.app) (Nb args [*]).')

args = parser.parse_args()

# Readind data
if args.filepath is not None:
    work = reader_orientation(args.filepath, args.skip)
    print("Orientation file reading done.")
else:
    print("The access road to the photogrammetric site is missing.")
    sys.exit()

# Add a projection to the worksite
work.set_proj(args.epsg, args.pathepsg, args.pathgeotiff)
print("Projection set-up.")

# Reading camera file
if args.camera is not None:
    read_camera(args.camera, work)
    print("Camera file reading done.")

# Add shape of image
if args.widthxheight is not None:
    for cam in work.cameras.values():
        cam.add_dim_image(args.widthxheight[0], args.widthxheight[1])

# Reading connecting point
if args.connecting_points is not None:
    read_copoints(args.connecting_points, work)
    print("Connecting point reading done.")

# Calculate ground coordinate of conneting point by intersection

# Reading GCP
if args.gcp is not None:
    read_gcp(args.gcp, work)
    print("GCP reading done.")

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp([3])

# Writing data
if args.writer is not None:
    manager_writer(args.writer, args.pathreturn, work)
    print(f"File written in {args.pathreturn + work.name}.{args.writer} .")
