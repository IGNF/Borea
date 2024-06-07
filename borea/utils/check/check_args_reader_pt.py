"""
A script for verification args to read a point file.
"""
from borea.utils.check.check_header import check_head, check_h_z, get_type_z_and_header


def check_header_file(header: list, type_pt: str) -> tuple:
    """
    Check if the header of the file is good.

    Args:
        header (list): List of column type file.
        type_pt (str): Type of point is reading (co_point, gcp2d, gcp3d).

    Returns:
        tuple: header, type_z
    """
    type_z = None
    list_letter = ['S', 'N', 'X', 'Y', 'Z', 'H', 'P', 'T']

    bad_head, ms_error_letter, _, symbol = check_head(header, list_letter)

    if type_pt in ["gcp3d", "pt3d"]:
        ll_type = ['P', 'T', 'X', 'Y', 'Z', 'H']
        misss = set(ll_type) - symbol
        if misss != set() and misss != set("T"):
            if "T" in misss:
                misss.remove("T")
            bad_head, ms_error_letter = check_h_z(bad_head, misss, ms_error_letter)
        if not bad_head:
            header, type_z = get_type_z_and_header(header)
    else:
        ll_type = ['P', 'N', 'X', 'Y']
        misss = set(ll_type) - symbol
        if misss != set():
            bad_head = True
            ms_error_letter += f"The letters {misss} are missing.\n"

    ms_error = "Your header is not correct.\n"
    ms_error += ms_error_letter
    if bad_head:
        raise ValueError(ms_error)

    return header, type_z
