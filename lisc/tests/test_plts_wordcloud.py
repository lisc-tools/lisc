"""Tests for the wordcloud plots from lisc."""

from nltk import FreqDist

from lisc.plts.wordcloud import *

###################################################################################################
###################################################################################################

def test_make_wc():

    freq_dist = FreqDist(['lots', 'of', 'words', 'words'])
    plot_wordcloud(freq_dist, 5, 'Name')
