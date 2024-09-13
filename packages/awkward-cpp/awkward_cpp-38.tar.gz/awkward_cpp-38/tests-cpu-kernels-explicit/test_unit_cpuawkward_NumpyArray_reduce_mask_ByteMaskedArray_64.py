# AUTO GENERATED ON 2024-09-12 AT 19:52:33
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import numpy as np
import pytest

from awkward_cpp.cpu_kernels import lib

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_1():
    toptr = []
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_2():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 30
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_3():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 30
    outlength = 10
    parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_4():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 30
    outlength = 6
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_5():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 18
    outlength = 6
    parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_6():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 21
    outlength = 6
    parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 4, 2, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_7():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 20
    outlength = 4
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_8():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 20
    outlength = 5
    parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_9():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 15
    outlength = 3
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_10():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 12
    outlength = 3
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_11():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 15
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_12():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 12
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_13():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 5
    parents = [0, 0, 0, 1, 1, 2, 2, 3, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_14():
    toptr = [123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 10
    outlength = 2
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_15():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 10
    outlength = 4
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_16():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 7
    outlength = 4
    parents = [0, 0, 0, 1, 1, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_17():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 10
    outlength = 4
    parents = [0, 0, 0, 1, 2, 2, 2, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_18():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 5
    parents = [0, 0, 3, 3, 1, 1, 4, 4, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_19():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 10
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_20():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 0, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_21():
    toptr = [123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 5
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_22():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 1, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_23():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 5
    outlength = 3
    parents = [0, 0, 1, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_24():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 6
    outlength = 3
    parents = [0, 1, 1, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_25():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 22
    outlength = 8
    parents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 5, 2, 6, 6, 6, 7]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 1, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_26():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 5
    parents = [0, 0, 0, 1, 2, 2, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_27():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 1, 1, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_28():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 12
    outlength = 9
    parents = [0, 0, 6, 6, 1, 1, 7, 7, 2, 2, 8, 8]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 0, 1, 1, 1, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_29():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 1, 1, 1, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_30():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 1, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_31():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_32():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_33():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 5
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_34():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 0, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_35():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 3
    outlength = 3
    parents = [0, 0, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_36():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    lenparents = 9
    outlength = 7
    parents = [0, 0, 0, 2, 2, 3, 6, 6, 6]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 0, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

