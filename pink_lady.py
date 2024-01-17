"""
pink lady launch module
"""
import sys
import argparse
import importlib
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_copoints import read_copoints
from src.reader.reader_gcp import read_gcp

parser = argparse.ArgumentParser(description='photogrammetric site conversion'
                                 + ' and manipulation software')
parser.add_argument('-f', '--filepath',
                    type=str, default=None, nargs=1,
                    help='File path of the workfile')
parser.add_argument('-skip', '--skip',
                    type=int, default=1, nargs=1,
                    help='Number of lines to be skipped before reading the file')
parser.add_argument('-epsg', '--epsg',
                    type=str, default='EPSG:2154', nargs=1,
                    help='EPSG codifier number of the reference system used ex: "EPSG:2154"')
parser.add_argument('-pepsg', '--pathepsg',
                    type=str, default=None, nargs=1,
                    help='Path to the json file which list the code epsg, you use')
parser.add_argument('-w', '--writer',
                    type=str, default=None,
                    help='Worksite output file format ex:opk')
parser.add_argument('-pr', '--pathreturn',
                    type=str, default='test/tmp/', nargs=1,
                    help='Conversion path ex:test/tmp/')
parser.add_argument('-c', '--camera',
                    type=str, default=None, nargs='*',
                    help='Files paths of cameras (xml or txt)')
parser.add_argument('-cp', '--connecting_points',
                    type=str, default=None, nargs='*',
                    help='Files paths of connecting points (.mes)')
parser.add_argument('-gcp', '--gcp',
                    type=str, default=None, nargs='*',
                    help='Files paths of GCP (.app)')

args = parser.parse_args()

# Readind data
if args.filepath[0] is not None:
    work = reader_orientation(args.filepath[0], args.skip)
    print("Orientation file reading done")
else:
    print("The access road to the photogrammetric site is missing")
    sys.exit()

# Add a projection to the worksite
if args.epsg[0] is not None:
    if args.pepsg is not None:
        work.set_proj(args.epsg[0], args.pepsg[0])
    else:
        work.set_proj(args.epsg[0])
else:
    work.set_proj()

# Reading camera file
if args.camera is not None:
    read_camera(args.camera, work)
    print("Camera file reading done")

# Reading connecting point
if args.connecting_points is not None:
    read_copoints(args.connecting_points, work)
    print("Connecting point reading done")

# Calculate ground coordinate of conneting point by intersection

# Reading GCP
if args.gcp is not None:
    read_gcp(args.connecting_points, work)
    print("GCP reading done")

# Calculate image coordinate of GCP if they exist
work.calculate_world_to_image_gcp([3])

# Writing data
if args.writer is not None:
    try:
        my_module = importlib.import_module("src.writer.writer_" + args.writer.lower())
        work = my_module.write(args.pathreturn, work)
    except ModuleNotFoundError as e:
        raise ValueError(f"{args.writer} file is not taken into account !!!") from e
