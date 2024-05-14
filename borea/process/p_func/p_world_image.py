"""
Args of parser to calcule image coordinate.
"""
import argparse
from borea.process.p_add_data.p_file_gcp2d import args_gcp2d, process_gcp2d
from borea.process.p_add_data.p_write import args_writer
from borea.worksite.worksite import Worksite
from borea.process.p_add_data.p_file_gcp3d import args_gcp3d, process_gcp3d
from borea.transform_world_image.transform_worksite.world_image_work import WorldImageWork
from borea.writer.writer_df_to_txt import write_df_to_txt


def args_world_image(parser: argparse) -> argparse:
    """
    Args to control photogrametrique file.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_gcp3d(parser)
    parser = args_gcp2d(parser)
    parser.add_argument('-d', '--control_type',
                        type=str, default=[], nargs='*',
                        help='Type of gcp to control.')
    parser = args_writer(parser)
    return parser


def process_world_image(args, work: Worksite) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Data.
    """
    # Read GCP 3D and 2D
    work = process_gcp3d(args, work)
    work = process_gcp2d(args, work)

    # Calculate image coordinate of GCP if they exist
    print("Calculation of data world to image.")
    WorldImageWork(work).calculate_world_to_image(args.control_type)

    df2d = work.get_point_image_dataframe("gcp3d", [])
    write_df_to_txt(args.namereturn, args.pathreturn, df2d)
