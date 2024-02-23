"""
Script test for module check array
"""
import numpy as np
from src.utils.check.check_array import check_array_transfo


def test_check_array_transfo_floatfloat():
    x = 1.0
    y = 1.0
    z = 1.0
    actual = check_array_transfo(x,y,z)
    assert type(actual[0]) == float
    assert type(actual[1]) == float
    assert type(actual[2]) == float


def test_check_array_transfo_arrayarray():
    x = np.array([1.0,1.0])
    y = np.array([1.0,1.0])
    z = np.array([1.0,1.0])
    actual = check_array_transfo(x,y,z)
    assert isinstance(actual[0], np.ndarray)
    assert isinstance(actual[0], np.ndarray)
    assert isinstance(actual[0], np.ndarray)


def test_check_array_transfo_arrayfloatdim1():
    x = np.array([1.0])
    y = np.array([1.0])
    z = np.array([1.0])
    actual = check_array_transfo(x,y,z)
    assert type(actual[0]) == float
    assert type(actual[1]) == float
    assert type(actual[2]) == float


def test_check_array_transfo_arrayfloatdim2():
    x = np.array([[1.0]])
    y = np.array([[1.0]])
    z = np.array([[1.0]])
    actual = check_array_transfo(x,y,z)
    assert type(actual[0]) == float
    assert type(actual[1]) == float
    assert type(actual[2]) == float


def test_check_array_transfo_arrayarraydim12():
    x = np.array([[1.0,1.0]])
    y = np.array([[1.0,1.0]])
    z = np.array([[1.0,1.0]])
    actual = check_array_transfo(x,y,z)
    assert (actual[0] == np.array([1.0,1.0])).all()
    assert (actual[1] == np.array([1.0,1.0])).all()
    assert (actual[2] == np.array([1.0,1.0])).all()


def test_check_array_transfo_arrayarraydim22():
    x = np.array([[1.0],[1.0]])
    y = np.array([[1.0],[1.0]])
    z = np.array([[1.0],[1.0]])
    actual = check_array_transfo(x,y,z)
    assert (actual[0] == np.array([1.0,1.0])).all()
    assert (actual[1] == np.array([1.0,1.0])).all()
    assert (actual[2] == np.array([1.0,1.0])).all()