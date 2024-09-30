"""
Main to transform projection of 3D points.
"""
# pylint: disable=import-error, wrong-import-position, line-too-long
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from borea.process.p_func.p_tf_proj_pt import args_tf_proj_param, process_tf_proj_param  # noqa: E402, E501


def transform_proj_pt():
    """
    Transforms the projection of a point file by pyproj.
    """
    parser = argparse.ArgumentParser(description='Transform coordinate projection of the 3D points'
                                                 ' file.')

    # Args
    parser = args_tf_proj_param(parser)

    args = parser.parse_args()

    # Process data
    process_tf_proj_param(args)


if __name__ == "__main__":
    transform_proj_pt()
