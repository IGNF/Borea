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
