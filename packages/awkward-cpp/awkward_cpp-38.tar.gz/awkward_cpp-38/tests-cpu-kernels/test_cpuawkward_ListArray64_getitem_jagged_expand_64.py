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

def test_cpuawkward_ListArray64_getitem_jagged_expand_64_1():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [1, 1, 1]
    pytest_multistops = [1, 1, 1]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_expand_64_2():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [2, 2, 2]
    pytest_multistops = [3, 3, 3]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_expand_64_3():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [2, 2, 2]
    pytest_multistops = [1, 1, 1]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_expand_64_4():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [1, 1, 1]
    pytest_multistops = [0, 0, 0]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_expand_64_5():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [0, 0, 0]
    pytest_multistops = [0, 0, 0]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

