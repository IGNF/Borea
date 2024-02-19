"""
Main to convert opk file to an other opk file
"""
import argparse
from src.parser.parser_opk.args_read_opk import args_ropk
from src.parser.parser_opk.args_write_opk import args_wopk
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.writer.manage_writer import manager_writer


parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                             ' and manipulation software opk to opk.')
parser = args_ropk(parser)
parser = args_wopk(parser)

args = parser.parse_args()

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
if args.dem is not None:
    work.add_dem(args.dem, args.fm)
    print("Add dem to the worksite done.")
else:
    print("Not Dem in the worksite.")

# Writing data
if args.name is not None:
    if args.output_header is not None:
        args_writing = {"header": args.output_header,
                        "unit_angle": args.output_unit_angle,
                        "linear_alteration": args.output_linear_alteration}
        manager_writer("opk", args.name, args.pathreturn, args_writing, work)
        print(f"File written in {args.pathreturn + args.name}.opk.")
    else:
        raise ValueError("The output header file is missing -o.")
else:
    raise ValueError("The name of the saving file is missing -n.")
