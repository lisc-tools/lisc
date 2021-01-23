"""Tests for the lisc.plts.counts."""

import numpy as np

from lisc import Counts

from lisc.tests.tutils import plot_test, optional_test

from lisc.plts.counts import *

###################################################################################################
###################################################################################################

@optional_test('seaborn')
@plot_test
def test_plot_matrix():

	# test with array input
    test_data = np.array([[1, 2], [3, 4]])
    plot_matrix(test_data, ['A', 'B'], ['C', 'D'])

    # test with Counts object input
    counts = Counts()
    counts.score =  test_data
    plot_matrix(counts, transpose=True)

@optional_test('seaborn')
@plot_test
def test_plot_clustermap():

	# test with array input
    test_data = np.array([[1, 2], [3, 4]])
    plot_clustermap(test_data)

    # test with Counts object input
    counts = Counts()
    counts.score =  test_data
    plot_clustermap(counts, transpose=True)

@optional_test('scipy')
@plot_test
def test_plot_dendrogram():

	# test with array input
    test_data = np.array([[1, 2], [3, 4]])
    plot_dendrogram(test_data, ['A', 'B'])

    # test with Counts object input
    counts = Counts()
    counts.score =  test_data
    plot_dendrogram(counts, transpose=True)
