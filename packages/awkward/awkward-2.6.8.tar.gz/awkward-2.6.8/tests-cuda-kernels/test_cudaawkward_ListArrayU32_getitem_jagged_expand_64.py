# AUTO GENERATED ON 2024-09-12 AT 19:52:33
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import cupy
import cupy.testing as cpt
import numpy as np
import pytest

import awkward as ak
import awkward._connect.cuda as ak_cu
from awkward._backends.cupy import CupyBackend

cupy_backend = CupyBackend.instance()

def test_cudaawkward_ListArrayU32_getitem_jagged_expand_64_1():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArrayU32_getitem_jagged_expand_64_2():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 2, 2]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [3, 3, 3]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArrayU32_getitem_jagged_expand_64_3():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 2, 2]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArrayU32_getitem_jagged_expand_64_4():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArrayU32_getitem_jagged_expand_64_5():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [0, 0, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

