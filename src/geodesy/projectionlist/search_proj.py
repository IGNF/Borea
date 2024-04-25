"""
Research data in ProjectionList.txt.
"""
import os


PATH_FILE = os.path.join(os.path.dirname(__file__), "ProjectionList.txt")


def convert_line_list(line: str) -> list:
    """
    Convert type of all element in list in str.

    Args:
        list_data(str): One line of file.

    Returns:
        list: List with str object.
    """
    return [x[1:-1] for x in line[1:-2].split(',')]


def search_info(type_input: str, data_input: str, type_output: str) -> str:
    """
    Research data in ProjectionList.txt.
    header: ["SD","BDORTHO","EPSG","GEOVIEW","MAPINFO","PROJ4","TA","TOPAERO","WKT"]

    Args:
        type_input (str): type of data input to refer.
        data_input (str): data to refer.
        type_output (str): type of data output to research.

    Returns:
        str: data output.
    """
    try:
        with open(PATH_FILE, 'r', encoding="utf-8") as file_proj:
            list_data = file_proj.readlines()
            header = convert_line_list(list_data[0])
            if type_input.upper() not in header and type_output.upper() not in header:
                raise ValueError(f"{type_input} or {type_output} not in header: {header}")

            id_input = header.index(type_input)
            id_output = header.index(type_output)

            for info_proj in list_data[1:]:
                data = convert_line_list(info_proj)
                if data[id_input] == "null" or data[id_output] == "null":
                    continue
                if data[id_input] == data_input:
                    data_research = data[id_output]
                    break

        file_proj.close()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The path {PATH_FILE} is incorrect !!!") from e

    if data_research == "null":
        return None
    return data_research
