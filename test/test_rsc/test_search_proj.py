"""
Test the module search_proj.py
"""
import pytest
from src.rsc.search_proj import search_info


def test_search_info():
    info = search_info("EPSG", "2154", "GEOVIEW")
    assert info == "LAMBERT93"


def test_search_info_bad_header():
    with pytest.raises(ValueError):
        search_info("LA", '3', "AL")