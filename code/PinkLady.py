import argparse
import code.Reader as r
import code.Writer as w

parser = argparse.ArgumentParser(description='photogrammetric site conversion and manipulation software')
parser.add_argument('-f', '--filepath',type=str, default= "", nargs=1, help='file path of the workfile')
parser.add_argument('-skip', '--skip', type=int, default=None, nargs=1, help='number of lines to be skipped before reading the file')

args = parser.parse_args()

if args.filepath != "":
    work = r.from_file(args.filepath, args.skip)
    print("File reading done")
else:
    print("The access road to the photogrammetric site is missing")

