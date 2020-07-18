"""Tests for the wordcloud plots from lisc."""

from nltk import FreqDist

from lisc.plts.wordcloud import *

###################################################################################################
###################################################################################################

def test_create_wordcloud():

    words = {'words' : 2, 'yay' : 3}
    wc = create_wordcloud(words)

    assert wc

def test_conv_freqs():

    freq_dist = FreqDist(['lots', 'of', 'words', 'words'])
    out = conv_freqs(freq_dist, 2)

    assert isinstance(out, dict)
