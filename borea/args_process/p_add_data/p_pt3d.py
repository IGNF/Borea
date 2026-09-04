"""
Args of parser for image coordinate of ground point
"""
import argparse
import numpy as np
from borea.transform_world_image.transform_shot.world_image_shot import WorldImageShot
from borea.worksite.worksite import Worksite


def args_add_pt3d(parser: argparse) -> argparse:
    """
    Args for 3D point

    Args:
        parser (argparse): Parser to add argument.

    Returns:
        argsparse: Parser with argument.
    """
    parser.add_argument('-p', '--point3d',
                        type=float, nargs=3,
                        help='Coordinate of the 3D point X Y Z.')
    parser.add_argument('-d', '--type_z_data',
                        type=str, default=None, choices=['altitude', 'height', None],
                        help='Unit of the z of the data.')

    return parser


def process_world_image(args: argparse, work: Worksite) -> None:
    """
    Processing args to calculate image coordinate of the point.

    Args:
        args (argparse): Arg to apply on worksite (data).
        work (Worksite): Worksite to work on.
    """
    work.set_type_z_data(args.type_z_data)

    coor2d = WorldImageShot(work.shots[args.name_shot],
                            work.cameras[list(work.cameras.keys())[0]]
                            ).world_to_image(np.array(args.point3d),
                                             work.type_z_data,
                                             work.type_z_shot)
    print(f"Image coordinate of the point 3D {args.point3d} is : {np.round(coor2d, 2)}")
    print("Data summary:")
    print(f"* position shot {work.shots[args.name_shot].pos_shot}")
    print(f"* orientation shot {work.shots[args.name_shot].ori_shot}")
