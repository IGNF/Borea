"""
Script to read GCP app.
"""
from pathlib import Path, PureWindowsPath
import numpy as np
from src.worksite.worksite import Worksite


def read_gcp(file: str, work: Worksite) -> None:
    """
    Read file gcp.

    Agrs:
        file (str): Path of file gcp.
        work (Worksite): Worksite which needs gcp.
    """
    try:
        with open(Path(PureWindowsPath(file)), 'r', encoding="utf-8") as file_gcp:
            for gcp in file_gcp.readlines():
                if gcp != '\n':
                    name_gcp, code_gcp, x, y, z = gcp.split()
                    work.add_gcp3d(name_gcp, int(code_gcp), np.array([float(x),
                                                                    float(y),
                                                                    float(z)]))
            file_gcp.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {file} is incorrect !!!") from e
    work.check_gcp = True
