"""
Script test for module writer df to txt
"""
import os
import pandas as pd
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_point import read_file_pt
from src.writer.writer_df_to_txt import write_df_to_txt


INPUT_OPK = "./dataset/23FD1305_alt_test.OPK"
INPUT_TERRAIN = "./dataset/terrain_test.mes"


def test_write_df_txt():
    work = reader_orientation(INPUT_OPK, {"order_axe":'opk',"interval": [2, None],"header": list("NXYZOPKC"),"unit_angle": "degree","linear_alteration":True})
    read_file_pt(INPUT_TERRAIN, list("PNXY"), "gcp2d", work)
    df = work.get_point_image_dataframe("gcp2d", [])
    write_df_to_txt("Test_pt", "./test/tmp/", df)
    assert os.path.exists("./test/tmp/Test_pt.txt")


def test_write_df_txt2():
    df = pd.DataFrame({'A':['A','B'],"one":1})
    write_df_to_txt("Test_pt2", "./test/tmp/", df)
    assert os.path.exists("./test/tmp/Test_pt2.txt")
