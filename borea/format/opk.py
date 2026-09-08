"""
Class to process Opk files
"""
import argparse
import os
from pathlib import Path
import platform
import numpy as np
from borea.args_process.p_add_data.p_gen_param import args_general_param, check_args_gen, process_args_gen_param
from borea.args_process.p_add_data.p_unit_shot import args_input_shot, args_output_shot
from borea.args_process.p_format.p_read_file import args_reading
from borea.args_process.p_format.p_write import args_writer
from borea.utils.check.check_header import get_type_z_and_header
from borea.utils.check.check_path import check_path
from borea.worksite.worksite import Worksite
from borea.utils.check.check_args import check_args_opk, check_header_file, check_output_input_args
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

    def check_args(self, args: argparse.Namespace) -> None:
        """
        Check arguments to read opk file

        Args:
            args (argparse.Namespace): All the function’s parameters.
        """
        if not os.path.exists(args.file_path):
            raise ValueError(f"The path to the OPK file is invalid: {args.file_path}")

        if args.first_line is None or args.first_line < 0:
            raise ValueError(f"The value first_line {args.first_line} is invalid; it must be > 0")

        args.header, args.type_z = check_header_file(args.header)

    def read(self, args: argparse.Namespace) -> Worksite:
        """
        Reads an opk file to transform it into a Workside object.

        Args:
            args (argparse.Namespace): Information for reading an opk file.
                        keys:
                        file_path (str): Path of the file.
                        order_axe (str): Order of rotation matrix axes.
                        first_line (int): First line to start to read the file.
                        last_line
                        header (list): List of column type file.
                        unit_angle (str): Unit of angle 'degrees' or 'radian'.
                        linear_alteration (bool): True if data corrected by linear alteration.

        Returns:
            Worksite: The worksite.
        """
        work = Worksite(Path(args.path_file).name)

        header = args.header

        try:
            with open(args.file_path, 'r', encoding="utf-8") as file_opk:
                for item_opk in file_opk.readlines()[args.first_line:args.last_line]:
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
                                      args.unit_angle, args.linear_alteration, args.order_axe)
                file_opk.close()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The path {args.file_path} is incorrect !!! "
                                    f"or your os is {platform.system()}. "
                                    "For Windows path is \\, "
                                    "for Linux and MacOS (Darwin) is / .") from e

        work.type_z_shot = args.type_z
        work = process_args_gen_param(args, work)
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
            arg (Namespace): Args of parser.
        """
        if args.output_header is not None:
            args.output_header, args.output_type_z = check_header_file(args.output_header)
        else:
            try:
                args.header
            except AttributeError:
                args.header = list("NXYZOPKC")
            args.output_header = args.header
            args.output_type_z = args.type_z

        check_output_input_args(args, "unit_angle", "output_unit_angle")
        check_output_input_args(args, "order_axe", "order_axe_output")
        check_output_input_args(args, "linear_alteration", "output_linear_alteration")
        check_output_input_args(args, "unit_angle", "output_unit_angle")

        cond_linear_alt = (args.output_linear_alteration is not None and
                           args.output_linear_alteration != args.linear_alteration)

        if args.type_z != args.output_type_z or cond_linear_alt:
            if args.epsg is None or args.pathgeoid is None:
                ms = "You must enter the EPSG code and path of geoîde to make the changes."
                raise ValueError(ms)

        if cond_linear_alt:
            check_args_gen(args)

    def write(self, args: argparse.Namespace, work: Worksite) -> None:
        """
        Write function, to save a photogrammetric site in .opk format.
    
        Args:
            args (argparse.Namespace): Information for writing an opk file.
                keys:
                "order_axe" (str): Order of rotation matrix axes,
                "header" (list): List of column type file.
                "unit_angle" (str): Unit of angle 'degree' or 'radian'.
                "linear_alteration" (bool): True if data corrected by linear alteration.
            work (Worksite): The site to be recorded.
        """
        path_opk = os.path.join(check_path(args.path_return), f"{args.name_return}.opk")
    
        if "S" in args.output_header:
            raise ValueError("Letter S doesn't existe in writing header opk.")
    
        work.set_unit_output(args.output_type_z,
                             args.unit_angle,
                             args.linear_alteration,
                             args.order_axe)
    
        header_file = ""
        for i in args.output_header:
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
                        line_writing += dict_letter[args.output_header[i]]
                        if i != 7:
                            line_writing += "   "
                        else:
                            line_writing += "\n"
    
                file.write(line_writing)
            file.close()
        except FileNotFoundError as e:
            raise ValueError("The path doesn't exist !!!", e) from e
