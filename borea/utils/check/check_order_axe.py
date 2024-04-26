"""
Script to check order axe and return axe for scipy
"""
from borea.utils.check.check_header import check_head


def check_order_axe(order_axe: str) -> str:
    """
    Check if code is good and convert for scipy rotation.

    Args:
        order_axe (str): Order of rotation matrix axes.

    Retuns:
        str: Order of ratation matrix axe for scipy.
    """
    list_val = ['o', 'p', 'k']

    bad_head, ms_error_letter, _, symbol = check_head(list(order_axe), list_val)

    misss = set(list_val) - symbol
    if misss != set():
        bad_head = True
        ms_error_letter += f"The letters {misss} are missing.\n"

    ms_error = "Your order axe is not correct.\n"
    ms_error += ms_error_letter
    if bad_head:
        raise ValueError(ms_error)

    return convert_opk_to_xyz(order_axe)


def convert_opk_to_xyz(order_axe: str) -> str:
    """
    Convert for scipy formalism.

    Args:
        order_axe (str): Order of rotation matrix axes.

    Retuns:
        str: Order of ratation matrix axe for scipy.
    """
    letter_conv = {"o": "x", "p": "y", "k": "z"}

    form_xyz = ""
    for i in order_axe:
        form_xyz += letter_conv[i]

    return form_xyz
