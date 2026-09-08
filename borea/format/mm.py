"""
Class to process MicMac files xml
"""
import argparse
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from borea.args_process.p_add_data.p_gen_param import args_general_param, process_args_gen_param
from borea.args_process.p_add_data.p_unit_shot import args_input_shot
from borea.args_process.p_format.p_read_file import args_reading
from borea.format.strategy.interface import FileReader
from borea.utils.check.check_header import get_type_z_and_header
from borea.utils.miscellaneous.miscellaneous import convert_3val_to_float
from borea.worksite.worksite import Worksite


class MmReader(FileReader):
    """
    Manager class of Micmac xml file reader
    """
    def args(self, parser: argparse) -> argparse:
        """
        Args for reading opk file.
    
        Args:
            parser (argparse): Parser to add argument.
    
        Returns:
            argsparse: Parser with argument.
        """
        parser = args_reading(parser)
        parser.add_argument('-i', '--type_z',
                            type=str, default=None,
                            choices=[None, "Z", "H"],
                            help='Type of z in data '
                            'Z for altitud and H for height.')
        parser = args_input_shot(parser)
        parser = args_general_param(parser)
        return parser

    def check_args(self, args: argparse.Namespace) -> None:
        """
        Check arguments to read opk file

        Args:
            args (argparse.Namespace): All the function’s parameters.
        """
        try:
            re.compile(Path(args.file_path).name)
        except re.error as error:
            raise ValueError(f"Le regex {args.file_path} n'est pas valide") from error

        if args.type_z in ["H", "Z"]:
            _, args.type_z = get_type_z_and_header(args.type_z)

    def read(self, args: argparse.Namespace) -> Worksite:
        """
        Reads an xml images to transform it into a Workside object.

        Args:
            path (Path): Regex to the path xml image worksite.
            work (Worksite): Worksite to add shot.

        Returns:
            Worksite: The worksite.
        """
        path = Path(args.file_path)
        regex = re.compile(path.name)
        path_dir = path.parent

        work = Worksite(path_dir.name)
        # browse all images
        for name_file in os.listdir(path_dir):
            if regex.match(name_file):
                tree = ET.parse(os.path.join(path_dir, name_file))
                root = tree.getroot()
                info_image = root.find("Data").find("CameraPose")
                # get name of image
                name_image = info_image.find("NameImage").text[1:-1]
                # get name of camera
                camera = info_image.find("NameInternalCalib").text[1:-1]
                # get position of image
                center = info_image.find("Center").text.split()
                xyz = np.array(convert_3val_to_float(center))
                # get rotation of image
                opk = info_image.find("WPK").text.strip().split(" ")
                opk = np.array(convert_3val_to_float(opk))
                # add shot
                work.add_shot(name_image, xyz, opk, camera, "degree",
                              True, "opk")

        work.type_z_shot = args.type_z
        work = process_args_gen_param(args, work)
        return work
