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

def test_check_aliases():

    kwargs = {'linewidth' : 3, 'color' : 'black'}

    assert check_aliases(kwargs, ['linewidth', 'lw']) == 3
    assert check_aliases(kwargs, ['markersize', 'ms']) == None
    assert check_aliases(kwargs, ['markersize', 'ms'], 10) == 10

@optional_test('seaborn')
def test_get_cmap():

    assert get_cmap('purple')
    assert get_cmap('blue')

    with raises(ValueError):
        get_cmap('Not a thing.')

def test_counts_data_helper():

    # Use custom test object and add data
    tcounts = Counts()

    terms_a = [['A'], ['B']]
    terms_b = [['C'], ['D']]

    tcounts.add_terms(terms_a, dim='A')
    tcounts.add_terms(terms_b, dim='B')

    counts = np.array([[1, 1], [2, 2]])
    score = np.array([[3, 3], [4, 4]])

    tcounts.counts = counts
    tcounts.score = score

    data, x_labels, y_labels = counts_data_helper(tcounts, None, None, 'counts', False)
    assert np.array_equal(data, counts)
    assert x_labels == tcounts.terms['B'].labels
    assert y_labels == tcounts.terms['A'].labels

    data, x_labels, y_labels = counts_data_helper(tcounts, None, None, 'score', True)
    assert np.array_equal(data, score.T)
    assert x_labels == tcounts.terms['A'].labels
    assert y_labels == tcounts.terms['B'].labels

@optional_test('matplotlib')
def test_check_ax():

    # Check None input
    ax = check_ax(None)
    assert ax == None

    # Check running with pre-created axis
    _, ax = plt.subplots()
    nax = check_ax(ax)
    assert nax == ax

    # Check creating figure of a particular size
    figsize = [5, 5]
    ax = check_ax(None, figsize=figsize)
    fig = plt.gcf()
    assert list(fig.get_size_inches()) == figsize
