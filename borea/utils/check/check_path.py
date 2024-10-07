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
    file = Path(file)
    name = file.stem

    if "/" in name:
        return Path(PurePosixPath(file))

    if "\\" in name:
        return Path(PureWindowsPath(file))

    return file
