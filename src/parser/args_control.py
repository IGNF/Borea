"""
Args of parser to control file
"""
import argparse


def args_control(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file

    Args:
        parser (argparse): parser to add argument

    Returns:
        argsparse: parser with argument
    """
    parser.add_argument('-l', '--connecting_points',
                        type=str, default=None, nargs='*',
                        help='Files paths of connecting points (.mes).')
    parser.add_argument('-t', '--ground_points',
                        type=str, default=None, nargs='*',
                        help='Files paths of ground points in images (.mes).')
    parser.add_argument('-g', '--gcp',
                        type=str, default=None, nargs='*',
                        help='Files paths of GCP (.app).')
    parser.add_argument('-d', '--control_type',
                        type=int, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser.add_argument('--fg', '--format_gcp',
                        type=str, default=None,
                        help='Format of GCP and ground image point "altitude" or "height".')
    return parser
