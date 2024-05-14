"""
Args of parser to calcule world coordinate.
"""
import argparse
from borea.process.p_add_data.p_write import args_writer
from borea.worksite.worksite import Worksite
from borea.process.p_add_data.p_file_gcp2d import args_gcp2d, process_gcp2d
from borea.transform_world_image.transform_worksite.image_world_work import ImageWorldWork
from borea.writer.writer_df_to_txt import write_df_to_txt


def args_image_world(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_gcp2d(parser)
    parser.add_argument('-p', '--process',
                        type=str, default="inter", choices=["inter", "square"],
                        help="Type of process for the function image to world,"
                             "intersection or least_square")
    parser = args_writer(parser)
    return parser


def process_image_world(args, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Read GCP 2D
    work = process_gcp2d(args, work)

    # Calculate ground coordinate of conneting point by intersection
    print("Calculation of data image to world.")
    ImageWorldWork(work).manage_image_world(type_point="gcp2d",
                                            type_process=args.process,
                                            control_type=None)
    df3d = work.get_point_world_dataframe("gcp2d", [])
    write_df_to_txt(args.namereturn, args.pathreturn, df3d)
