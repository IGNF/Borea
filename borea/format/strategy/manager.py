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

        Args:
            parser (argparse): Parser for parameter.
            input_format (str): Input type of format.
            output_format (str): Output type of format.

        Return:
            Parser with argument for parameter
        """
        reader = self._registry.get_reader(input_format)
        writer = self._registry.get_writer(output_format)

        parser = reader.args(parser)
        parser = writer.args(parser)
        return parser

    def check_args(self, args: argparse.Namespace,
                   input_format: str, output_format: str) -> None:
        """
        Check args for request

        Args:
            args (argparse.Namespace): Parameter.
            input_format (str): Input type of format.
            output_format (str): Output type of format.
        """
        reader = self._registry.get_reader(input_format)
        writer = self._registry.get_writer(output_format)

        reader.check_args(args)
        writer.check_args(args)

    def convert(self, args: argparse.Namespace,
                input_format: str, output_format: str) -> None:
        """
        Convert input_format to output_format

        Args:
            args (argparse.Namespace): Parameter.
            input_format (str): Input type of format.
            output_format (str): Output type of format.
        """
        reader = self._registry.get_reader(input_format)
        writer = self._registry.get_writer(output_format)

        work = reader.read(args)
        writer.write(args, work)
