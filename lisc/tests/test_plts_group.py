"""Tests for the group plots from lisc."""

import numpy as np

from lisc.tests.utils import plot_test

from lisc.plts.group import *

###################################################################################################
###################################################################################################

@plot_test
def test_plot_matrix():

    test_dat = np.array([[1, 2], [3, 4]])

    plot_matrix(test_dat, ['A', 'B'], ['C', 'D'])

@plot_test
def test_plot_clustermap():

    test_dat = np.array([[1, 2], [3, 4]])
    plot_clustermap(test_dat)

@plot_test
def test_plot_dendrogram():

    test_dat = np.array([[1, 2], [3, 4]])
    plot_dendrogram(test_dat, ['A', 'B'])
