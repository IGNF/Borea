"""
Class to convert orientation file
"""
import argparse

from borea.format.strategy.registry import FormatRegistry


class FormatManager:
    """
    Orchestrator class to manage the request of conversion format
    """
    def __init__(self, registry: FormatRegistry):
        self._registry = registry

    def add_args(self, parser: argparse,
                 input_format: str, output_format: str) -> argparse:
        """
        Add to parser arguments to read input_format and to write output format 
        """
        reader = self._registry.get_reader(input_format)
        writer = self._registry.get_writer(output_format)

        parser = reader.args(parser)
        parser = writer.args(parser)
        return parser

    def convert(self, path: str, input_format: str,
                path_output: str, output_format: str) -> None:
        """
        Convert input_format to output_format
        """
        reader = self._registry.get_reader(input_format)
        writer = self._registry.get_writer(output_format)

        document = reader.read(path)
        writer.write(document, path_output)
