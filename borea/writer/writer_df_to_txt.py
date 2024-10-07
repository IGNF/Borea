"""
Photogrammetry worksite to writing dataframe to txt.
"""
import os
import pandas as pd
from borea.utils.check.check_path import check_path


def write_df_to_txt(name: str, pathreturn: str, df: pd.DataFrame) -> None:
    """
    Writing DataFrame to txt in column.

    Args:
        name (str): Name of the file.
        pathreturn (str): Path to save the file.
        df (pd.DataFrame): DataFrame to save.
    """
    path_txt = os.path.join(check_path(pathreturn), f"{name}.txt")

    name_column = list(df.columns)

    with open(path_txt, "w", encoding="utf-8") as file:
        for _, row in df.iterrows():
            wline = ""
            for id_col in name_column:
                if not isinstance(row[id_col], float):
                    wline += f"{row[id_col]} "
                else:
                    wline += f"{round(row[id_col], 3)} "
            wline += "\n"
            file.write(wline)
        file.close()
