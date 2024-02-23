"""
A script for verification header str in manage reader.
"""


def check_header_file(header: list) -> tuple:
    """
    Check if the header of the file is good

    Args:
        header (list): List of column type file.

    Returns:
        tuple: header without type, type of z, type of angle
    """
    list_letter = ['S', 'N', 'X', 'Y', 'Z', 'H', 'O', 'P', 'K', 'C']
    bad_head = False
    ms_error_letter = ""
    symbol = set()
    head = []

    for l_type in header:
        if l_type[0] in list_letter:
            if l_type[0] not in head or l_type[0] == "S":
                head.append(l_type[0])
                if l_type[0] != "S":
                    symbol.add(l_type[0])
            else:
                bad_head = True
                ms_error_letter += f"Symbol {l_type[0]} appears several times, "
                ms_error_letter += "this is incorrect, must appear only once\n"
        else:
            bad_head = True
            ms_error_letter += f"Symbol {l_type[0]} is not recognized, "
            ms_error_letter += f"list of symbol recognized {list_letter}\n"

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
        tuple: header and type_z
    """
    if "H" in header:
        type_z = "height"
        header[header.index('H')] = "Z"
    else:
        type_z = "altitude"

    return header, type_z