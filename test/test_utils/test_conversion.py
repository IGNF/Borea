"""
Script test for module convedrtion
"""
import numpy as np
from src.utils.conversion import check_array_transfo, change_dim


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


def test_change_dim_floatfloat():
    x = 0
    dim = ()
    actual = change_dim(x, dim)
    assert actual == 0


def test_change_dim_array12array21():
    x = np.array([[0,0]])
    dim = (2,1)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (2,1)


def test_change_dim_floatarray1():
    x = 0
    dim = (1,)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (1,)


def test_change_dim_array1float():
    x = np.array([1.0])
    dim = ()
    actual = change_dim(x, dim)
    assert np.shape(actual) == ()


def test_change_dim_array1array1():
    x = np.array([1.0])
    dim = (1,)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (1,)


def test_change_dim_floatarray11():
    x = 0
    dim = (1,1)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (1,1)


def test_change_dim_array2array12():
    x = np.array([0,0])
    dim = (1,2)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (1,2)


def test_change_dim_array2array21():
    x = np.array([0,0])
    dim = (2,1)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (2,1)
    