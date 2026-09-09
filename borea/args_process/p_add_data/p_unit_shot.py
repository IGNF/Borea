"""
Args of parser for unit of shot
"""
import argparse


def args_input_shot(parser: argparse) -> argparse:
    """
    Args for reading opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-b', '--order_axe_input',
                        type=str, default=None,
                        help="Order of rotation matrix axes.")
    parser.add_argument('-u', '--unit_angle',
                        type=str, default=None, choices=['degree', 'radian', None],
                        help="Unit of the angle of shooting, 'degree' or 'radian'.")
    parser.add_argument('-a', '--linear_alteration',
                        type=bool, default=None,
                        help="True if z shot corrected by linear alteration.")
    return parser


def check_args_shot(args: argparse.Namespace) -> None:
    """
    Checking the arguments of input args shot.

    Args:
        arg (Namespace): Args of parser.
    """
    if args.order_axe_input is None:
        raise ValueError("Parameter -b --order_axe_input must be completed.")
    if args.unit_angle is None:
        raise ValueError("Parameter -u --unit_angle must be completed.")
    if args.linear_alteration is None:
        raise ValueError("Parameter -a --linear_alteration must be completed.")


def args_output_shot(parser: argparse) -> argparse:
    """
    Args for reading opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('--ob', '--order_axe_output',
                        type=str, default=None,
                        help="Order of rotation matrix axes you want in output.")
    parser.add_argument('--ou', '--output_unit_angle',
                        type=str, default=None, choices=["degree", "radian", None],
                        help="Unit of the angle of shooting, 'degree' or 'radian'")
    parser.add_argument('--oa', '--output_linear_alteration',
                        type=bool, default=None,
                        help="True if z shot corrected by linear alteration.")
    return parser
