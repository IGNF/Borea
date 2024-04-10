"""
Script test for module reader for file point
"""
import pytest
import numpy as np
import pandas as pd
from src.reader.orientation.manage_reader import reader_orientation
from src.reader.reader_point import read_file_pt, read_file_pt_dataframe

class TestReaderFilePt:
    @classmethod
    def setup_class(cls):
        INPUT_OPK = "./dataset/23FD1305_alt_test.OPK"
        ARGS = {"order_axe":'opk',
                "interval": [2, None],
                "header": list("NXYZOPKC"),
                "unit_angle": "degree",
                "linear_alteration":True}
        cls.work = reader_orientation(INPUT_OPK, ARGS)
        cls.INPUT_TERRAIN = "./dataset/terrain_test.mes"
        cls.INPUT_GCP = "./dataset/GCP_test.app"
        cls.INPUT_LIAISONS = "./dataset/liaisons_test.mes"


    def test_read_gcp2d(self):
        read_file_pt(self.INPUT_TERRAIN, list("PNXY"), "gcp2d", self.work)
        assert self.work.gcp2d['"1003"'] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
        assert self.work.gcp2d['"1005"'] == ["23FD1305x00054_05680", "23FD1305x00054_05681"]
        assert self.work.gcp2d['"1006"'] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
        assert (self.work.shots["23FD1305x00026_01306"].gcp2d['"1003"'] == [24042.25, 14781.17]).all()
        assert (self.work.shots["23FD1305x00026_01307"].gcp2d['"1003"'] == [24120.2, 10329.3]).all()
        assert (self.work.shots["23FD1305x00026_01308"].gcp2d['"1003"'] == [24161.49, 5929.37]).all()
        assert (self.work.shots["23FD1305x00054_05680"].gcp2d['"1005"'] == [22796.05, 14371.27]).all()
        assert (self.work.shots["23FD1305x00054_05681"].gcp2d['"1005"'] == [22817.4, 9930.73]).all()
        assert (self.work.shots["23FD1305x00062_07727"].gcp2d['"1006"'] == [20209.92, 16200.26]).all()
        assert (self.work.shots["23FD1305x00062_07728"].gcp2d['"1006"'] == [20329.12, 11794.01]).all()


    def test_read_gcp(self):
        read_file_pt(self.INPUT_GCP, list("PTXYZ"), "gcp3d", self.work)
        assert list(self.work.gcp3d) == ['"1003"','"1005"','"1006"']
        assert self.work.gcp3d['"1003"'].name_gcp == '"1003"'
        assert self.work.gcp3d['"1003"'].code == "13"
        assert (self.work.gcp3d['"1003"'].coor == np.array([815601.510, 6283629.280, 54.960])).all()
        assert self.work.gcp3d['"1005"'].name_gcp == '"1005"'
        assert self.work.gcp3d['"1005"'].code == "3"
        assert (self.work.gcp3d['"1005"'].coor == np.array([833670.940, 6281965.400, 52.630])).all()
        assert self.work.gcp3d['"1006"'].name_gcp == '"1006"'
        assert self.work.gcp3d['"1006"'].code == "13"
        assert (self.work.gcp3d['"1006"'].coor == np.array([838561.350, 6284600.330, 62.470])).all()
    

    def test_read_gcpt(self):
        with pytest.raises(ValueError) as e_info:
            read_file_pt(self.INPUT_GCP, list("PXYZ"), "gcp3d", self.work)


    def test_read_co_points(self):
        read_file_pt(self.INPUT_LIAISONS, list("PNXY"), "co_point", self.work)
        assert self.work.co_points["MES_674214"] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
        assert self.work.co_points["MES_674219"] == ["23FD1305x00026_01306", "23FD1305x00026_01307", "23FD1305x00026_01308"]
        assert self.work.co_points["MES_264193"] == ["23FD1305x00062_07727", "23FD1305x00062_07728"]
        assert (self.work.shots["23FD1305x00026_01306"].co_points["MES_674214"] == [3885.75, 14969.14]).all()
        assert (self.work.shots["23FD1305x00026_01306"].co_points["MES_674219"] == [3896.99, 13858.47]).all()
        assert (self.work.shots["23FD1305x00026_01306"].co_points["MES_674216"] == [6033.01, 16208.41]).all()
        assert (self.work.shots["23FD1305x00054_05680"].co_points["MES_145568"] == [559.85, 7656.41]).all()
        assert (self.work.shots["23FD1305x00054_05680"].co_points["MES_145570"] == [436.4, 6604.65]).all()
        assert (self.work.shots["23FD1305x00062_07727"].co_points["MES_264192"] == [4009.15, 5334.46]).all()
        assert (self.work.shots["23FD1305x00062_07727"].co_points["MES_264193"] == [1956.18, 5550.03]).all()
    

    def test_read_file_pt_dataframe_co_point(self):
        df = read_file_pt_dataframe(self.INPUT_LIAISONS,list("PNXY"),"pt2d")
        assert (df == pd.DataFrame({"id_pt":["MES_674214","MES_674214","MES_674214","MES_674216","MES_674216","MES_674216","MES_674219","MES_674219","MES_674219","MES_145568","MES_145568","MES_145570","MES_145570","MES_264192","MES_264192","MES_264193","MES_264193"],
                                    "id_shot":["23FD1305x00026_01306","23FD1305x00026_01307","23FD1305x00026_01308","23FD1305x00026_01306","23FD1305x00026_01307","23FD1305x00026_01308","23FD1305x00026_01306","23FD1305x00026_01307","23FD1305x00026_01308","23FD1305x00054_05680","23FD1305x00054_05681","23FD1305x00054_05680","23FD1305x00054_05681","23FD1305x00062_07727","23FD1305x00062_07728","23FD1305x00062_07727","23FD1305x00062_07728"],
                                    "column":[3885.75,3952.47,3987.46,6033.01,6105.62,6142.4,3896.99,3958.87,3992.63,559.85,562.3,436.4,438.06,4009.15,4105.73,1956.18,2053.55],
                                    "line":[14969.14,10617.99,6251.46,16208.41,11854.17,7490.99,13858.47,9507.56,5142.34,7656.41,3206.21,6604.65,2162.62,5334.46,926.9,5550.03,1147.48]})).all
        
    
    def test_read_file_pt_dataframe_gcp3d(self):
        df = read_file_pt_dataframe(self.INPUT_GCP,list("PTXYZ"),"pt3d")
        assert (df == pd.DataFrame({"id_pt":["1003","1005","1006"],
                                    "type":[13,3,13],
                                    "x":[815601.510,833670.940,838561.350],
                                    "y":[6283629.280,6281965.400,6284600.330],
                                    "z":[54.960,52.630,62.470]})).all
    

    def test_read_file_pt_dataframe_gcp3dt(self):
        df = read_file_pt_dataframe(self.INPUT_GCP,list("PXYZ"),"pt3d")
        assert (df == pd.DataFrame({"id_pt":["1003","1005","1006"],
                                    "type":None,
                                    "x":[815601.510,833670.940,838561.350],
                                    "y":[6283629.280,6281965.400,6284600.330],
                                    "z":[54.960,52.630,62.470]})).all
