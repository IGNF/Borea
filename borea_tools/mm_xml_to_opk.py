"""
Main to convert Micmac xml files to an opk file
"""
# pylint: disable=import-error, wrong-import-position, line-too-long
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_add_data.p_write import args_writer  # noqa: E402
from borea.reader.orientation.manage_reader import reader_orientation  # noqa: E402
from borea.writer.manage_writer import manager_writer  # noqa: E402


def mm_xml_to_opk():
    """
    Converts an orientation file into an OPK file.
    Support OPK file and MicMac output (folder of xml files).
    """
    parser = argparse.ArgumentParser(description='Photogrammetric site conversion'
                                                 ' and manipulation software opk to opk.')
    # Args for implement opk to opk
    parser.add_argument('-r', '--filepath',
                        type=str, help='File path of the workfile.')
    parser = args_writer(parser)
    parser.add_argument('-o', '--output_header',
                        type=str, default=None,
                        help='Type of each column in the site file.'
                        'e.g. NXYZOPKC'
                        'N: name of shot'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position'
                        'O: omega rotation angle'
                        'P: phi rotation angle'
                        'K: kappa rotation angle'
                        'C: name of the camera')

    args = parser.parse_args()

    # Process to read data
    if args.filepath is not None:
        fake_param = {"order_axe": "opk",
                      "linear_alteration": True}
        work = reader_orientation(args.filepath, fake_param)
        print("Orientation file reading done.")
        print(f"Number of image: {len(work.shots)}")
    # Check output header
    if args.output_header and "H" in args.output_header:
        args.output_header[args.output_header.index('H')] = "Z"
    # Process to write opk
    print("Writing OPK.")
    if args.namereturn is not None:
        args_writing = {"order_axe": 'opk',
                        "header": args.output_header,
                        "unit_angle": 'degree',
                        "linear_alteration": True}
        manager_writer("opk", args.namereturn, args.pathreturn, args_writing, work)
        print(f"File written in {args.pathreturn + args.namereturn}.opk.")
    else:
        raise ValueError("The name of the saving file is missing -n.")


if __name__ == "__main__":
    mm_xml_to_opk()
