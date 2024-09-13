# AUTO GENERATED ON 2024-09-12 AT 19:52:33
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import numpy as np
import kernels

def test_pyawkward_localindex_64_1():
    toindex = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_localindex_64')
    funcPy(toindex=toindex, length=length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

