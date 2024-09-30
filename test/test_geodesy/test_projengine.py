"""
Script test for module proj_engine
"""
# pylint: disable=import-error, missing-function-docstring, unused-argument, duplicate-code
import pyproj
import pytest
import pandas as pd
from borea.datastruct.dtm import Dtm
from borea.geodesy.proj_engine import ProjEngine


PATH_CSV = "./dataset/GCP_test.app"
EPSG = [2154]
PATH_GEOID = ["./dataset/fr_ign_RAF20.tif"]
EPSG_OUTPUT = 4326


def setup_module(module):  # run before the first test
    Dtm.clear()
    ProjEngine.clear()


def test_projengine_notgeoid():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG)
    with pytest.raises(ValueError):
        _ = ProjEngine().tf.geog_to_geoid


def test_projengine_notgeoidwithpathgeotiff():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, ["fr_ign_RAF2.tif"])
    with pytest.raises(pyproj.exceptions.ProjError):
        _ = ProjEngine().tf.geog_to_geoid


def test_get_meridian_convergence():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, PATH_GEOID)
    proj = ProjEngine()
    meridian_convergence = proj.get_meridian_convergence(815601, 6283629)
    theorical_value = -1.039350
    assert abs(meridian_convergence - theorical_value) < 0.000001


def test_tf_create_tf_output():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, PATH_GEOID, 4326)
    proj = ProjEngine()
    assert proj.tf.proj_to_proj_out


def test_tf_conv_tf_output():
    ProjEngine.clear()
    ProjEngine().set_epsg(EPSG, PATH_GEOID, 4326)
    proj = ProjEngine()
    xf = 657945.43
    yf = 6860369.44
    ym = 2.427
    xm = 48.842
    xmo, ymo = proj.tf.proj_to_proj_out(xf, yf)
    assert round(xmo, 3) == xm
    assert round(ymo, 3) == ym


def test_transform_proj():
    df = pd.read_csv(PATH_CSV, sep=' ',
                     skiprows=0,
                     usecols=[0, 1, 2, 3, 4],
                     index_col=False,
                     names=["id_pnt", "type", "x", "y", "z"],
                     dtype={"id_pnt": str,
                            "type": int,
                            "x": float,
                            "y": float,
                            "z": float})
    ProjEngine().set_epsg(EPSG, epsg_output=EPSG_OUTPUT)
    df_proj = ProjEngine().tf.transform_pt_proj(df)
    assert round(df_proj.loc[0, "x"], 3) == 43.642
    assert round(df_proj.loc[0, "y"], 3) == 4.432
    assert df_proj.loc[0, "z"] == 54.96
    assert round(df_proj.loc[1, "x"], 3) == 43.624
    assert round(df_proj.loc[1, "y"], 3) == 4.656
    assert df_proj.loc[1, "z"] == 52.63
    assert round(df_proj.loc[2, "x"], 3) == 43.647
    assert round(df_proj.loc[2, "y"], 3) == 4.717
    assert df_proj.loc[2, "z"] == 62.47


def test_transform_proj_zh():
    df = pd.read_csv(PATH_CSV, sep=' ',
                     skiprows=0,
                     usecols=[0, 1, 2, 3, 4],
                     index_col=False,
                     names=["id_pnt", "type", "x", "y", "z"],
                     dtype={"id_pnt": str,
                            "type": int,
                            "x": float,
                            "y": float,
                            "z": float})
    type_z = "altitude"
    type_z_output = "height"
    ProjEngine().set_epsg(EPSG, PATH_GEOID, EPSG_OUTPUT)
    df_proj = ProjEngine().tf.transform_pt_proj(df, type_z, type_z_output)
    assert round(df_proj.loc[0, "x"], 3) == 43.642
    assert round(df_proj.loc[0, "y"], 3) == 4.432
    assert df_proj.loc[0, "z"] != 54.96
    assert round(df_proj.loc[1, "x"], 3) == 43.624
    assert round(df_proj.loc[1, "y"], 3) == 4.656
    assert df_proj.loc[1, "z"] != 52.63
    assert round(df_proj.loc[2, "x"], 3) == 43.647
    assert round(df_proj.loc[2, "y"], 3) == 4.717
    assert df_proj.loc[2, "z"] != 62.47
