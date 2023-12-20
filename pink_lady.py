"""
pink lady launch module
"""
import argparse

from code.reader import from_file
from code.writer import to_opk

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

args = parser.parse_args()


if args.filepath[0] != "":
    work = from_file(args.filepath[0], args.skip)
    print("File reading done")
else:
    print("The access road to the photogrammetric site is missing")

print(args.writer)

if args.writer == 'opk':
    to_opk(args.pathreturn[0], work)
    print('file save well')
