"""Tests for the lisc.analysis.counts."""

from pytest import raises

import numpy as np

from lisc.analysis.counts import *

###################################################################################################
###################################################################################################

def test_compute_normalization():

    data = np.array([[10, 10, 10], [20, 20, 20]])
    counts_a = [1, 2]
    counts_b = [1, 2, 5]

    out = compute_normalization(data, counts_a, 'A')
    assert np.array_equal(out, np.array([[10, 10, 10], [10, 10, 10]]))

    out = compute_normalization(data, counts_b, 'B')
    assert np.array_equal(out, np.array([[10, 5, 2], [20, 10, 4]]))

    # Test error if data shapes are inconsistent
    with raises(ValueError):
        compute_normalization(data, counts_b, 'A')

    # Test error if the 'dim' input is bad
    with raises(ValueError):
        compute_normalization(data, counts_b, 'C')

def test_compute_association_index():

    data = np.array([[5, 10, 5], [0, 5, 0]])
    counts_a = [10, 10]
    counts_b = [10, 10, 10]

    out = compute_association_index(data, counts_a, counts_b)
    assert np.array_equal(out, np.array([[5/(20-5), 10/(20-10), 5/(20-5)],
                                         [0/(20-0), 5/(20-5), 0/(20-0)]]))

    # Test error if data shapes are not consistent
    with raises(ValueError):
        compute_association_index(data, counts_b, counts_a)

def test_compute_similarity():

    data = np.array([[5, 10, 5], [0, 5, 0]])

    out = compute_similarity(data)

    # Test that diagonal values are 1
    assert np.all(np.isclose(np.diag(out), 1.))

    # Test that non-diagonal values are not 1
    assert np.all(out[np.where(~np.eye(out.shape[0], dtype=bool))] != 1.)
