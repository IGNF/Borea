"""
Args of parser for reading opk file
"""
import argparse
from borea.args_process.p_add_data.p_gen_param import args_general_param, process_args_gen_param
from borea.args_process.p_add_data.p_unit_shot import args_input_shot
from borea.worksite.worksite import Worksite
from borea.reader.orientation.manage_reader import reader_orientation


def args_reading(parser: argparse) -> argparse:
    """
    Args for reading opk file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    # pylint: disable=duplicate-code
    parser.add_argument('-r', '--file_path', required=True,
                        type=str, help='File path of the workfile.')
    return parser


# ---- Process args ----
def process_args_read(args: argparse) -> Worksite:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data)

    Returns:
        Worksite: data
    """
    # Reading data
    if args.file_path is not None:
        if args.header is not None:
            work = reader_orientation(args.file_path, {"order_axe": args.order_axe_input.lower(),
                                                      "interval": [args.first_line, args.last_line],
                                                      "header": list(args.header.upper()),
                                                      "unit_angle": args.unit_angle,
                                                      "linear_alteration": args.linear_alteration})
            print("Orientation file reading done.")
            print(f"Number of image: {len(work.shots)}")
        else:
            raise ValueError("The header file is missing -i.")
    else:
        raise ValueError("The access road to the photogrammetric site is missing -r.")

    work = process_args_gen_param(args, work)

    return work