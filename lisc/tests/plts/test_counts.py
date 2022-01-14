"""Tests for the lisc.plts.counts."""

import numpy as np

from lisc import Counts

from lisc.tests.tutils import plot_test, optional_test

from lisc.plts.counts import *

###################################################################################################
###################################################################################################

@optional_test('seaborn')
@plot_test
def test_plot_matrix(tdb):

    # test with array input
    test_data = np.array([[1, 2], [3, 4]])
    plot_matrix(test_data, ['A', 'B'], ['C', 'D'], file_name='test_matrix1.pdf', directory=tdb)

    # test with Counts object input
    counts = Counts()
    counts.score = test_data
    plot_matrix(counts, transpose=True, file_name='test_matrix2.pdf', directory=tdb)

@optional_test('seaborn')
@plot_test
def test_plot_vector(tdb):

    # test with array input
    test_data = np.array([1, 2 , 3, 4])
    plot_vector(test_data, file_name='test_vector1.pdf', directory=tdb)

    # test with Counts object input
    counts = Counts()
    counts.terms['A'].counts = test_data
    plot_vector(counts, file_name='test_matrix2.pdf', directory=tdb)

@optional_test('seaborn')
@plot_test
def test_plot_clustermap(tdb):

    # test with array input
    test_data = np.array([[1, 2], [3, 4]])
    plot_clustermap(test_data, file_name='test_clustermap1.pdf', directory=tdb)

    # test with Counts object input
    counts = Counts()
    counts.score = test_data
    plot_clustermap(counts, transpose=True, file_name='test_clustermap2.pdf', directory=tdb)

@optional_test('scipy')
@plot_test
def test_plot_dendrogram(tdb):

    # test with array input
    test_data = np.array([[1, 2], [3, 4]])
    plot_dendrogram(test_data, ['A', 'B'], file_name='test_dendro1.pdf', directory=tdb)

    # test with Counts object input
    counts = Counts()
    counts.terms['B']._labels = ['A', 'B']
    counts.score = test_data
    plot_dendrogram(counts, transpose=True, file_name='test_dendro1.pdf', directory=tdb)
