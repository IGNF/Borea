"""
Script test for module change dim
"""
import numpy as np
from src.utils.change_dim import change_dim


def test_change_dim_floatfloat():
    x = np.array([0])
    dim = ()
    actual = change_dim(x, dim)
    assert actual == 0


def test_change_dim_array12array21():
    x = np.array([[0,0]])
    dim = (2,1)
    actual = change_dim(x, dim)
    assert np.shape(actual) == (2,1)


def test_change_dim_floatarray1():
    x = np.array([0])
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
    x = np.array([0])
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
    