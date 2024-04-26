"""
Args of parser for world coordinate of image point
"""
import argparse
import numpy as np
from borea.transform_world_image.transform_shot.image_world_shot import ImageWorldShot
from borea.worksite.worksite import Worksite


def args_add_pt2d(parser: argparse) -> argparse:
    """
    Args for 2D point

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-p', '--point2d',
                        type=float, nargs=2,
                        help='Coordinate of the 2D point Column Line.')
    parser.add_argument('-d', '--type_z_data',
                        type=str, default=None, choices=['altitude', 'height', None],
                        help='Unit of the z of the data in output.')

    return parser


def process_image_world(args: argparse, work: Worksite) -> None:
    """
    Processing args to calculate world coordinate of the point.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Worksite to work on.
    """
    work.set_type_z_data(args.type_z_data)

    coor3d = ImageWorldShot(work.shots[args.name_shot],
                            work.cameras[list(work.cameras.keys())[0]]
                            ).image_to_world(np.array(args.point2d),
                                             work.type_z_data,
                                             work.type_z_shot)
    print(f"World coordinate of the point 2D {args.point2d} is : {np.round(coor3d, 2)}")
    print("Data summary:")
    print(f"* position shot {work.shots[args.name_shot].pos_shot}")
    print(f"* orientation shot {work.shots[args.name_shot].ori_shot}")
