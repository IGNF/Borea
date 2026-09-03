"""
OFC Orientation File Conversion

Type input reading: OPK, Mimac xml
Type output writing: OPK, RPC, Conl
"""
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


READING = ["opk", "mm"]
WRITING = ["opk", "rpc", "conl"]

def writing_type_subparsers(top_subparsers, name):

    return top_subparsers

def reading_type_subparsers(top_subparsers, name):
    parser_read = top_subparsers.add_parser(name, help=f"{name} type file to read")
    subparsers = parser_read.add_subparsers(title="Type output file",
                                            dest="type_output_file",
                                            required=True)
    return top_subparsers

def ofc():
    """
    OFC Orientation File Conversion

    Type input reading: OPK, Mimac xml
    Type output writing: OPK, RPC, Conl
    """
    parser = argparse.ArgumentParser(description="Orientation File Conversion")
    input_subparsers = parser.add_subparsers(title="Type input file",
                                             description="Type input file to read (OPK, MM)",
                                             dest="type_input_file",
                                             required=True)

    for type_read in READING:
        input_subparsers = reading_type_subparsers(input_subparsers, type_read)
    parser_check = input_subparsers.add_parser("OPK", help="OPK type file to read")
    opk_subparsers = parser_check.add_subparsers(dest="subcommand", required=True)


if __name__ == "__main__":
    ofc()
