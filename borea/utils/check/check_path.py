"""
Script to check path of data.
"""
from pathlib import Path, PureWindowsPath, PurePosixPath


def check_path(file: str) -> Path:
    """
    Check path of data if Posix of Windows path.

    Args:
        file (str): The path of data.

    Returns:
        Path: The good path.
    """
    if "/" in file:
        return Path(PurePosixPath(file))

    if "\\" in file:
        return Path(PureWindowsPath(file))

    return file
