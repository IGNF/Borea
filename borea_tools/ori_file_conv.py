"""
OFC Orientation File Conversion

Type input reading: OPK, Mimac xml
Type output writing: OPK, RPC, Conl
"""
import argparse
import sys
import os



sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.format.mm import MmReader
from borea.format.opk import OpkReader, OpkWriter
from borea.format.conl import ConlWriter
from borea.format.rpc import RpcWriter
from borea.format.strategy.manager import FormatManager
from borea.format.strategy.registry import FormatRegistry


def build_registry() -> FormatRegistry:
    """
    Build format registry for reader and writer
    """
    registry = FormatRegistry()

    # READER
    registry.register_reader("opk", OpkReader())
    registry.register_reader("mm", MmReader())

    # WRITER
    registry.register_writer("opk", OpkWriter())
    registry.register_writer("rpc", RpcWriter())
    registry.register_writer("conl", ConlWriter())

    return registry


def ofc():
    """
    OFC Orientation File Conversion

    Type input reading: OPK, Mimac xml
    Type output writing: OPK, RPC, Conl
    """
    registry = build_registry()
    format_manager = FormatManager(registry)

    # Build argparser
    parser = argparse.ArgumentParser(description="Orientation File Conversion")
    input_subparsers = parser.add_subparsers(title="Type input file",
                                             description="Type input file to read (OPK, MM)",
                                             dest="type_input_file",
                                             required=True)
    # Args for input file
    for type_read in registry.supported_inputs():
        parser_read = input_subparsers.add_parser(type_read, help=f"{type_read} type file to read")
        output_parsers = parser_read.add_subparsers(title="Type output file",
                                                    description="Type input file to write (OPK, RPC, CONL)",
                                                    dest="type_output_file",
                                                    required=True)
        # Args for output file
        for type_write in registry.supported_outputs():
            parser_read = output_parsers.add_parser(type_write, help=f"{type_write} type file to write")
            format_manager.add_args(parser_read, type_read, type_write)

    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    ofc()
