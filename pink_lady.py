"""
pink lady launch module
"""
import argparse
import importlib
from src.reader.orientation.manage_reader import reader_orientation
from src.writer.writer_opk import to_opk

parser = argparse.ArgumentParser(description='photogrammetric site conversion'
                                 + ' and manipulation software')
parser.add_argument('-f', '--filepath',
                    type=str, default="", nargs=1,
                    help='File path of the workfile')
parser.add_argument('-skip', '--skip',
                    type=int, default=None, nargs=1,
                    help='Number of lines to be skipped before reading the file')
parser.add_argument('-w', '--writer',
                    type=str, choices=['opk'],
                    help='Worksite output file format')
parser.add_argument('-pr', '--pathreturn',
                    type=str, default="test/tmp/", nargs=1,
                    help='Conversion path ex:"test/tmp/"')
parser.add_argument('-c', '--camera',
                    type=list, default=[], nargs='*',
                    help='Files paths of cameras')

args = parser.parse_args()

# Readind data
if args.filepath[0] != "":
    work = reader_orientation(args.filepath[0], args.skip)
    print("File reading done")
else:
    print("The access road to the photogrammetric site is missing")

# Reading camera file



# Writing data
try:
    my_module = importlib.import_module("src.reader.reader_" + args.writer.lower())
    work = my_module.write(args.pathreturn, work)
except ModuleNotFoundError as e:
    raise ValueError(f"{args.writer} file is not taken into account !!!") from e
