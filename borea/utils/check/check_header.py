"""
A script for verification header list str.
"""


def check_head(header: list, check_letter: list) -> tuple:
    """
    Checks that the header contains all the letters in the check letter.

    Args:
        header (list): List of column type file.
        check_letter (list): List of good letter in header.

    Returns:
        tuple: bad_head, ms_error, head, symbol
    """
    bad_head = False
    ms_error_letter = ""
    symbol = set()
    head = []

    for l_type in header:
        if l_type in check_letter:
            if l_type not in head or l_type == "S":
                head.append(l_type)
                if l_type != "S":
                    symbol.add(l_type)
            else:
                bad_head = True
                ms_error_letter += f"Symbol {l_type} appears several times, "
                ms_error_letter += "this is incorrect, must appear only once\n"
        else:
            bad_head = True
            ms_error_letter += f"Symbol {l_type} is not recognized, "
            ms_error_letter += f"list of symbol recognized {check_letter}\n"

    return bad_head, ms_error_letter, head, symbol


def check_h_z(bad_head: bool, misss: set, ms_error_letter: str) -> tuple:
    """
    Check letter H and Z in header.

    Args:
        bad_head (bool): boolean if the header is false.
        misss (set): Diff between list_letter and symbol.
        ms_error_letter (str): Error message.

    Returns:
        tuple: bad_head, ms_error_letter
    """
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

    return bad_head, ms_error_letter


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
