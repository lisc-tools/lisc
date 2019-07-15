"""Test for the analysis functions for counts, for LISC."""

from py.test import raises

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

    # Test error is shapes don't work
    with raises(ValueError):
        compute_normalization(data, counts_b, 'A')

    # Test error for if dimension specifier is bad
    with raises(ValueError):
        compute_normalization(data, counts_b, 'C')

def test_compute_association_index():

    data = np.array([[5, 10, 15], [0, 5, 10]])
    counts_a = [10, 10]
    counts_b = [10, 10, 10]

    out = compute_association_index(data, counts_a, counts_b)
    assert np.array_equal(out, np.array([[5/20, 10/20, 15/20], [0/20, 5/20, 10/20]]))

    # Test error is shapes don't work
    with raises(ValueError):
        compute_association_index(data, counts_b, counts_a)
