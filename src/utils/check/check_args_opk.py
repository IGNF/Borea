"""
A script for verification header str in manage reader.
"""
from src.utils.check.check_header import check_head


def check_args_opk(args: dict) -> tuple:
    """
    Check args for reading an oopk.

    Args:
        args (dict): Information for reading an opk file.
                     keys:
                     "interval" (list): Interval of lines taken into account,
                     [i, j] if i or j is None = :. e.g. [1, None] = [1:].
                     "header" (list): List of column type file.
                     "unit_angle" (str): Unit of angle 'degrees' or 'radian'.
                     "linear_alteration" (bool): True if data corrected by linear alteration.

    Return:
        tuple: args, header and type of z shot.
    """
    if args["unit_angle"] not in ["degree", "radian"]:
        raise ValueError(f"Unit angles is incorrect {args['unit_angle']},"
                         "correct writing is degree or radian.")

    if args["interval"][0] is not None and args["interval"][0] > 0:
        args["interval"][0] -= 1
    if args["interval"][1] is not None:
        args["interval"][1] -= 1

    header, type_z = check_header_file(args["header"])

    return args, header, type_z


def check_header_file(header: list) -> tuple:
    """
    Check if the header of the file is good.

    Args:
        header (list): List of column type file.

    Returns:
        tuple: Header without type, type of z, type of angle.
    """
    list_letter = ['S', 'N', 'X', 'Y', 'Z', 'H', 'O', 'P', 'K', 'C']

    bad_head, ms_error_letter, head, symbol = check_head(header, list_letter)

    misss = set(list_letter[1:]) - symbol
    if misss != {"Z"} and misss != {"H"} and misss != set():
        bad_head = True
        if "Z" in misss and "H" in misss:
            miss = misss.copy()
            miss.remove("Z")
            miss.remove("H")
            ms_error_letter += f"The letters 'Z' or 'H' are missing and lettres {miss}.\n"
        elif "Z" in misss:
            misss.remove("Z")
            ms_error_letter += f"The letters {misss} are missing.\n"
        else:
            misss.remove("H")
            ms_error_letter += f"The letters {misss} are missing.\n"

    if misss == set():
        bad_head = True
        ms_error_letter += "The letters Z and H cannot be in the same string.\n"

    ms_error = "Your header is not correct.\n"
    ms_error += ms_error_letter
    if bad_head:
        raise ValueError(ms_error)

    return get_type_z_and_header(head)


def get_type_z_and_header(header: list) -> tuple:
    """
    Return type of z, height if H and altitude if Z
    and header with the H replaced by a Z.

    Args:
        header (list): List of column type file.

    Returns:
        tuple: Header and type_z.
    """
    if "H" in header:
        type_z = "height"
        header[header.index('H')] = "Z"
    else:
        type_z = "altitude"

    return header, type_z
