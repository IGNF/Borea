"""
Args of parser to write file.
"""
import argparse


def args_writer(parser: argparse) -> argparse:
    """
    Args to write file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-n', '--namereturn',
                        type=str,
                        help='Name of the new file.')
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    return parser
