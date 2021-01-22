"""Tests for the lisc.plts.utils."""

from py.test import raises

import numpy as np

from lisc import Counts

from lisc.tests.tutils import optional_test

from lisc.plts.utils import *

###################################################################################################
###################################################################################################

def test_check_args():

    assert check_args(['new_name'], None) == {}
    assert check_args(['new_name'], [1, 2, 3]) == {'new_name' : [1, 2, 3]}

@optional_test('seaborn')
def test_get_cmap():

    assert get_cmap('purple')
    assert get_cmap('blue')

    with raises(ValueError):
        get_cmap('Not a thing.')

def test_counts_data_helper():

    # Use custom test object and add data
    tcounts = Counts()

    counts = np.array([[1, 1], [2, 2]])
    score = np.array([[3, 3], [4, 4]])
    tcounts.counts = counts
    tcounts.score = score

    terms_a = [['A'], ['B']]
    terms_b = [['C'], ['D']]
    a_labels = terms_a[0] + terms_a[1]
    b_labels = terms_b[0] + terms_b[1]
    tcounts.terms['A'].terms = a_labels
    tcounts.terms['B'].terms = b_labels

    data, x_labels, y_labels = counts_data_helper(tcounts, None, None, 'counts', False)
    assert np.array_equal(data, counts)
    assert x_labels == b_labels
    assert y_labels == a_labels

    data, x_labels, y_labels = counts_data_helper(tcounts, None, None, 'score', True)
    assert np.array_equal(data, score.T)
    assert x_labels == a_labels
    assert y_labels == b_labels

@optional_test('matplotlib')
def test_check_ax():

    # Check None input
    ax = check_ax(None)

    # Check running with pre-created axis
    _, ax = plt.subplots()
    nax = check_ax(ax)
    assert nax == ax

    # Check creating figure of a particular size
    figsize = [5, 5]
    ax = check_ax(None, figsize=figsize)
    fig = plt.gcf()
    assert list(fig.get_size_inches()) == figsize
