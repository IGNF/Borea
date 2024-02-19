"""
Args of parser for writing opk file
"""
import argparse


def args_wopk(parser: argparse) -> argparse:
    """
    Args for writing opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    # pylint: disable=duplicate-code
    parser.add_argument('-n', '--name',
                        type=str,
                        help='Name of the new file.')
    parser.add_argument('-w', '--pathreturn',
                        type=str, default='./',
                        help='Conversion path e.g. test/tmp/.')
    parser.add_argument('-o', '--output_header',
                        type=str,
                        help='Type of each column in the site file.'
                        'e.g. "N X Y Z O P K C"'
                        'N: name of shot'
                        'X: coordinate x of the shot position'
                        'Y: coordinate y of the shot position'
                        'Z: coordinate z of the shot position in altitude'
                        'H: coordinate z of the shot position in height'
                        'O: omega rotation angle'
                        'P: phi rotation angle'
                        'K: kappa rotation angle'
                        'C: name of the camera')
    parser.add_argument('-d', '--output_unit_angle',
                        type=str, default="degree",
                        help="Unit of the angle of shooting, 'degree' or 'radian'")
    parser.add_argument('-l', '--output_linear_alteration',
                        type=bool, default=True,
                        help="True if z shot corrected by linear alteration.")
    return parser
