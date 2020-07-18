"""Tests for the counts plots from lisc."""

import numpy as np

from lisc.tests.utils import plot_test, optional_test

from lisc.plts.counts import *

###################################################################################################
###################################################################################################

@optional_test('seaborn')
@plot_test
def test_plot_matrix():

    test_dat = np.array([[1, 2], [3, 4]])

    plot_matrix(test_dat, ['A', 'B'], ['C', 'D'])

@optional_test('seaborn')
@plot_test
def test_plot_clustermap():

    test_dat = np.array([[1, 2], [3, 4]])
    plot_clustermap(test_dat)

@optional_test('scipy')
@plot_test
def test_plot_dendrogram():

    test_dat = np.array([[1, 2], [3, 4]])
    plot_dendrogram(test_dat, ['A', 'B'])
