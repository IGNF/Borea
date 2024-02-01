"""
pink lady launch module
"""
import sys
import argparse
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gipoints import read_gipoints
from src.reader.reader_gcp import read_gcp
from src.writer.manage_writer import manager_writer

parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                             ' and manipulation software.')
parser.add_argument('-f', '--filepath',
                    type=str, help='File path of the workfile.')
parser.add_argument('-s', '--skip',
                    type=int, default=1,
                    help='Number of lines to be skipped before reading the file.')
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
parser.add_argument('-o', '--writer',
                    type=str, default=None,
                    help='Worksite output file format e.g. opk.')
parser.add_argument('-r', '--pathreturn',
                    type=str, default='./',
                    help='Conversion path e.g. test/tmp/.')
parser.add_argument('-c', '--camera',
                    type=str, default=None, nargs='*',
                    help='Files paths of cameras (xml or txt).')
parser.add_argument('-w', '--width',
                    type=int, default=None,
                    help='Width and height of the camera.')
parser.add_argument('-a', '--height',
                    type=float, default=None,
                    help='Width and height of the camera.')
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
                    type=int, default=None, nargs='*',
                    help='Type of gcp to control.')

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
if args.width is not None and args.height is not None:
    for cam in work.cameras.values():
        cam.add_dim_image(args.width, args.height)

# Reading connecting point
if args.connecting_points is not None:
    read_copoints(args.connecting_points, work)
    print("Connecting point reading done.")

# Reading ground point image
if args.ground_points is not None:
    read_gipoints(args.ground_points, work)
    print("Connecting point reading done.")

# Calculate ground coordinate of conneting point by intersection

# Reading GCP
if args.gcp is not None:
    read_gcp(args.gcp, work)
    print("GCP reading done.")

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp(args.control_type)

# Writing data
if args.writer is not None:
    manager_writer(args.writer, args.pathreturn, work)
    print(f"File written in {args.pathreturn + work.name}.{args.writer} .")
