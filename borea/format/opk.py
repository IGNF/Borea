"""
Class to process Opk files
"""
import argparse
import os
from pathlib import Path
import platform
import numpy as np
from borea.args_process.p_add_data.p_gen_param import args_general_param
from borea.args_process.p_add_data.p_unit_shot import args_input_shot, args_output_shot
from borea.args_process.p_format.p_read_file import args_reading
from borea.args_process.p_format.p_write import args_writer
from borea.utils.check.check_path import check_path
from borea.worksite.worksite import Worksite
from borea.utils.check.check_args import check_args_opk, check_header_file
from borea.format.strategy.interface import FileReader, FileWriter


class OpkReader(FileReader):
    """
    Manager class of opk reader
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
        parser.add_argument('-i', '--header',
                            type=str, default="NXYZOPKC",
                            help='Type of each column in the site file.'
                            'e.g. NXYZOPKC'
                            'S: to ignore the column'
                            'N: name of shot'
                            'X: coordinate x of the shot position'
                            'Y: coordinate y of the shot position'
                            'Z: coordinate z of the shot position in altitude'
                            'H: coordinate z of the shot position in height'
                            'O: omega rotation angle'
                            'P: phi rotation angle'
                            'K: kappa rotation angle'
                            'C: name of the camera')
        parser.add_argument('-f', '--first_line',
                            type=int, default=1,
                            help='Line number to start file playback. First line in the file is 1.'
                                    ' Does not take file header into account.')
        parser.add_argument('-z', '--last_line',
                            type=int, default=None,
                            help='Line number to end file playback.'
                                    ' If not set, all lines below -f will be read.')
        parser = args_input_shot(parser)
        parser = args_general_param(parser)
        return parser

    def read(self, file: Path, args: dict, work: Worksite) -> Worksite:
        """
        Reads an opk file to transform it into a Workside object.

        Args:
            file (Path): Path to the worksite.
            args (dict): Information for reading an opk file.
                        keys:
                        "order_axe" (str): Order of rotation matrix axes,
                        "interval" (list): Interval of lines taken into account,
                        [i, j] if i or j is None = :. e.g. [1, None] = [1:].
                        "header" (list): List of column type file.
                        "unit_angle" (str): Unit of angle 'degrees' or 'radian'.
                        "linear_alteration" (bool): True if data corrected by linear alteration.
            work (Worksite): Worksite to add shot.

        Returns:
            Worksite: The worksite.
        """
        args, header, type_z = check_args_opk(args)

        try:
            with open(file, 'r', encoding="utf-8") as file_opk:
                for item_opk in file_opk.readlines()[args["interval"][0]:args["interval"][1]]:
                    if item_opk != '\n' and item_opk[0] != '#':
                        item_shot = item_opk.split()
                        if len(item_shot) != len(header):
                            raise ValueError(f"The number of columns in your file {len(item_shot)}"
                                            " is different from the number of columns in your input"
                                            f" format {len(header)}.")
                        work.add_shot(item_shot[header.index("N")],
                                    np.array([float(item_shot[header.index("X")]),
                                                float(item_shot[header.index("Y")]),
                                                float(item_shot[header.index("Z")])], dtype=float),
                                    np.array([float(item_shot[header.index("O")]),
                                                float(item_shot[header.index("P")]),
                                                float(item_shot[header.index("K")])], dtype=float),
                                    item_shot[header.index("C")],
                                    args["unit_angle"], args["linear_alteration"], args["order_axe"])
                file_opk.close()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The path {file} is incorrect !!! "
                                    f"or your os is {platform.system()}. "
                                    "For Windows path is \\, "
                                    "for Linux and MacOS (Darwin) is / .") from e

        work.type_z_shot = type_z
        return work


class OpkWriter(FileWriter):
    """
    Manager class of opk writer
    """
    def args(self, parser: argparse) -> argparse:
        """
        Args for writing opk file.
    
        Args:
            parser (argparse): Parser to add argument.
    
        Returns:
            argsparse: Parser with argument.
        """
        # pylint: disable=duplicate-code
        parser = args_writer(parser)
        parser.add_argument('-o', '--output_header',
                            type=str, default=None,
                            help='Type of each column in the site file.'
                            'e.g. NXYZOPKC'
                            'N: name of shot'
                            'X: coordinate x of the shot position'
                            'Y: coordinate y of the shot position'
                            'Z: coordinate z of the shot position in altitude'
                            'H: coordinate z of the shot position in height'
                            'O: omega rotation angle'
                            'P: phi rotation angle'
                            'K: kappa rotation angle'
                            'C: name of the camera')
        parser = args_output_shot(parser)
        return parser

    def check_args(self, args: argparse.Namespace) -> None:
        """
        Checking the arguments to ensure that the request is achievable.

        Args:
            arg (Namespace): Arg of parser.
        """
        

    def write(self, name_opk: str, path_opk: str, args: dict, work: Worksite) -> None:
        """
        Write function, to save a photogrammetric site in .opk format.
    
        Args:
            name_opk (str): Name of the file writing.
            path_opk (str): Path of folder to registration file .opk.
            args (dict): Information for writing an opk file.
                         keys:
                         "order_axe" (str): Order of rotation matrix axes,
                         "header" (list): List of column type file.
                         "unit_angle" (str): Unit of angle 'degree' or 'radian'.
                         "linear_alteration" (bool): True if data corrected by
                         linear alteration.
            work (Worksite): The site to be recorded.
        """
        path_opk = os.path.join(check_path(path_opk), f"{name_opk}.opk")
    
        if args["header"]:
            header, type_z = check_header_file(args["header"])
        else:
            header = ['N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
            type_z = work.type_z_shot
    
        if "S" in header:
            raise ValueError("Letter S doesn't existe in writing header opk.")
    
        work.set_unit_output(type_z, args["unit_angle"], args["linear_alteration"], args["order_axe"])
    
        header_file = ""
        for i in header:
            header_file += i + "   "
    
        try:
            with open(path_opk, "w", encoding="utf-8") as file:
                file.write(header_file)
                file.write("\n")
                keys = np.sort(list(work.shots))
                line_writing = ""
                for k in keys:
                    shot = work.shots[k]
                    dict_letter = {"N": shot.name_shot,
                                   "X": str(shot.pos_shot[0]),
                                   "Y": str(shot.pos_shot[1]),
                                   "Z": str(shot.pos_shot[2]),
                                   "O": str(shot.ori_shot[0]),
                                   "P": str(shot.ori_shot[1]),
                                   "K": str(shot.ori_shot[2]),
                                   "C": shot.name_cam}
                    for i in range(8):
                        line_writing += dict_letter[header[i]]
                        if i != 7:
                            line_writing += "   "
                        else:
                            line_writing += "\n"
    
                file.write(line_writing)
            file.close()
        except FileNotFoundError as e:
            raise ValueError("The path doesn't exist !!!", e) from e
