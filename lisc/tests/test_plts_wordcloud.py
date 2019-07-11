"""Tests for the wordcloud plots from lisc."""

from nltk import FreqDist

from lisc.tests.utils import plot_test, optional_test

from lisc.plts.wordcloud import *

###################################################################################################
###################################################################################################

@optional_test('wordcloud')
@plot_test
def test_make_wc():

    freq_dist = FreqDist(['lots', 'of', 'words', 'words'])
    plot_wordcloud(freq_dist, 5, 'Name')
