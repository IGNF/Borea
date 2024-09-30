"""
Args of parser to transform projection of 3D points.
"""
import argparse

from borea.process.p_add_data.p_file_gcp3d import args_gcp3d
from borea.process.p_add_data.p_proj import args_proj_param
from borea.process.p_add_data.p_write import args_writer
from borea.reader.reader_point import read_file_pt_dataframe
from borea.geodesy.proj_engine import ProjEngine
from borea.writer.writer_df_to_txt import write_df_to_txt


def args_tf_proj_param(parser: argparse) -> argparse:
    """
    Args for adding transform proj of points parameter.

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser = args_gcp3d(parser)
    parser = args_proj_param(parser)
    parser.add_argument('--oz', '--z_output',
                        type=str, choices=[None, 'altitude', 'height'], default=None,
                        help="Output type of z. altitude or height")
    parser = args_writer(parser)
    return parser


def process_tf_proj_param(args: argparse) -> None:
    """
    Processing args with data.

    Args:
        args (argparse): Arg to apply on worksite (data).
    """
    # Read file to Dataframe
    df, type_z = read_file_pt_dataframe(args.gcp3d, args.head_gcp3d, "pt3d")

    # Setup Projection
    ProjEngine().set_epsg([args.epsg, args.geog, args.geoc], args.pathgeoid, args.oe)

    # Change projection
    new_df = ProjEngine().tf.transform_pt_proj(df, type_z, args.oz)

    # Write the new file
    write_df_to_txt(args.namereturn, args.pathreturn, new_df)
