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
                    type=str, default='', nargs=1,
                    help='File path of the workfile')
parser.add_argument('-skip', '--skip',
                    type=int, default=None, nargs=1,
                    help='Number of lines to be skipped before reading the file')
parser.add_argument('-w', '--writer',
                    type=str, default='',
                    help='Worksite output file format ex:opk')
parser.add_argument('-pr', '--pathreturn',
                    type=str, default='test/tmp/', nargs=1,
                    help='Conversion path ex:test/tmp/')
parser.add_argument('-c', '--camera',
                    type=str, default='', nargs='*',
                    help='Files paths of cameras (xml or txt)')
parser.add_argument('-cp', '--connecting_points',
                    type=str, default='', nargs='*',
                    help='Files paths of connecting points (.mes)')
parser.add_argument('-gcp', '--gcp',
                    type=str, default='', nargs='*',
                    help='Files paths of GCP (.app)')

args = parser.parse_args()

# Readind data
if args.filepath[0] != '':
    work = reader_orientation(args.filepath[0], args.skip)
    print("Orientation file reading done")
else:
    print("The access road to the photogrammetric site is missing")
    sys.exit()

# Reading camera file
if args.camera != '':
    read_camera(args.camera, work)
    print("Camera file reading done")

# Reading connecting point
if args.connecting_points != '':
    read_copoints(args.connecting_points, work)
    print("Connecting point reading done")

# Calculate ground coordinate of conneting point by intersection

# Reading GCP
if args.gcp != '':
    read_gcp(args.connecting_points, work)
    print("GCP reading done")

# Calculate image coordinate of GCP if they exist
work.calculate_coor_img_gcp()

# Writing data
if args.writer != '':
    try:
        my_module = importlib.import_module("src.writer.writer_" + args.writer.lower())
        work = my_module.write(args.pathreturn, work)
    except ModuleNotFoundError as e:
        raise ValueError(f"{args.writer} file is not taken into account !!!") from e
