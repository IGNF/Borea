"""
Function to implement xml.
"""
import xml.etree.ElementTree as ET
import numpy as np


def format_xml(elem: any, prec: str = ".5f") -> str:
    """
    Write item in xml format.

    Args:
        elem (any): The element to write in xml format.
        prec (str): Precision of the element if is a number.

    Returns:
        str: elem in xml format.
    """
    if isinstance(elem, float) and np.isnan(elem):
        return "0.00000"
    if isinstance(elem, (float, np.float32, np.float64)):
        return f"{elem:{prec}}"
    if elem is None:
        return ""

    return f"{elem}"


def indent(elem: ET, level: int = 0) -> None:
    """
    Structure the xml file.

    Args:
        elem (ET): The xml to write.
        level (int): Level of structure.
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def add_elem(xml: ET, balises: list, vals: list, prec: str = ".5f") -> None:
    """
    Add a list of element to the ET.

    Args:
        xml (ET): The xml to add elem.
        balises (list): List of name of the balise.
        vals (list): List of item to put on.
        prec (str): Precision of the element if is a number.
    """
    for balise, val in zip(balises, vals):
        ET.SubElement(xml, balise).text = format_xml(val, prec)
