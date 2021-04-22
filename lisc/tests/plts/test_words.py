"""Tests for lisc.plts.words."""

from collections import Counter

from lisc.tests.tutils import plot_test, optional_test

from lisc.plts.words import *

###################################################################################################
###################################################################################################

@optional_test('wordcloud')
@plot_test
def test_plot_wordcloud(tdb):

    freq_dist = Counter(['lots', 'of', 'words', 'words'])
    plot_wordcloud(freq_dist, 5, file_name='test_wordcloud.pdf', directory=tdb)

@optional_test('matplotlib')
@plot_test
def test_plot_years(tdb):

    years = Counter([2000, 2000, 2015, 2016])
    plot_years(years, year_range=[1999, 2017], file_name='test_years.pdf', directory=tdb)
