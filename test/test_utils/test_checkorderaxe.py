"""
Script test for module check_order_axe
"""
# pylint: disable=import-error, missing-function-docstring
import pytest
from borea.utils.check.check_order_axe import check_order_axe


def test_orcer_axe():
    xyz = check_order_axe("opk")
    yxz = check_order_axe("pok")
    zyx = check_order_axe("kpo")
    assert xyz == "xyz"
    assert yxz == "yxz"
    assert zyx == "zyx"


def test_bad_order():
    with pytest.raises(ValueError):
        check_order_axe("opkp")
    with pytest.raises(ValueError):
        check_order_axe("opi")
