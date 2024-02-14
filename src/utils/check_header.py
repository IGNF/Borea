"""
A script for verification header str in manage reader.
"""


# pylint: disable-next=too-many-locals too-many-branches too-many-statements
def check_header_file(header: list) -> tuple:
    """
    Check if the header of the file is good

    Args:
        header (list): List of column type file.

    Returns:
        tuple: header without type, type of z, type of angle
    """
    list_letter = ['S', 'N', 'X', 'Y', 'Z', 'O', 'P', 'K', 'C']
    list_suffix_z = ['h', 'hl', 'a', 'al']
    list_suffix_angle = ['d', 'r']
    bad_head = False
    ms_error_letter = ""
    ms_error_z = ""
    ms_error_angle = ""
    symbol = set()
    count_d = 0
    count_r = 0
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

        if l_type[0] == "Z":
            if l_type[1:] in list_suffix_z:
                type_z = l_type[1:]
            else:
                bad_head = True
                ms_error_z += f"The suffix '{l_type[1:]}' for Z is not recognized,"
                ms_error_z += f"list of symbol recognized {list_suffix_z}\n"

        if l_type[0] in ['O', 'P', 'K']:
            if l_type[1:] == 'd':
                count_d += 1
                type_angle = l_type[1:]
            elif l_type[1:] == 'r':
                count_r += 1
                type_angle = l_type[1:]
            else:
                bad_head = True
                ms_error_angle += f"The suffix '{l_type[1:]}' for angle is not recognized,"
                ms_error_angle += f"list of symbol recognized {list_suffix_angle}.\n"

    misss = set(list_letter[1:]) - symbol
    if misss != set():
        bad_head = True
        ms_error_letter += f"The letters {misss} are missing.\n"

    if not (count_r == 3 or count_d == 3):
        bad_head = True
        ms_error_angle += "There is no type for the angles, or they are different or not good.\n"
        ms_error_angle += "All three angles must have the same 'd' or 'r' unit."

    ms_error = "Your header is not correct.\n"
    ms_error += ms_error_letter + ms_error_z + ms_error_angle
    if bad_head:
        raise ValueError(ms_error)

    return head, type_z, type_angle
