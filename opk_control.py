"""
Main to control opk file
"""
import argparse
from src.parser.parser_opk.args_read_opk import args_ropk
from src.parser.args_control import args_control
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_camera import read_camera
from src.reader.reader_gipoints import read_ground_image_points
from src.reader.reader_gcp import read_gcp
from src.stat.statistics import Stat

parser = argparse.ArgumentParser(description='Photogrammetric site control opk file')
parser = args_ropk(parser)
parser = args_control(parser)

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

# Reading ground point image
if args.ground_points is not None:
    read_ground_image_points(args.ground_points, work)
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
print(f" in {args.pathreturn}Stat_module_{work.name}.txt .")
