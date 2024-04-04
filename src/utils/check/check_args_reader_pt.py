"""
A script for verification args to read a point file.
"""
from src.utils.check.check_header import check_head


def check_args_reader_pt(header: list, type_point: str) -> None:
    """
    Check if args for function reader file pt is good.

    Args:
        header (list): List of column type file.
        type_point (str): Type of point is reading (co_point, gcp2d, gcp3d).
    """
    if type_point not in ["co_point", "gcp2d", "gcp3d"]:
        raise ValueError(f"type {type_point} in incorrect. ['co_point', 'gcp2d', 'gcp3d']")

    check_header_file(header, type_point)


def check_header_file(header: list, type_pt: str) -> None:
    """
    Check if the header of the file is good.

    Args:
        header (list): List of column type file.
        type_point (str): Type of point is reading (co_point, gcp2d, gcp3d).
    """
    list_letter = ['S', 'N', 'X', 'Y', 'Z', 'P', 'T']

    bad_head, ms_error_letter, _, symbol = check_head(header, list_letter)

    if type_pt == "gcp3d":
        ll_type = ['P', 'T', 'X', 'Y', 'Z']
    else:
        ll_type = ['P', 'N', 'X', 'Y']

    misss = set(ll_type) - symbol
    if misss != set() and misss != set("T"):
        bad_head = True
        ms_error_letter += f"The letters {misss} are missing.\n"

    ms_error = "Your header is not correct.\n"
    ms_error += ms_error_letter
    if bad_head:
        raise ValueError(ms_error)
