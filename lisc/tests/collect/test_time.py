"""Tests for lisc.collect.time."""

from lisc.objects.counts import Counts1D
from lisc.objects.words import Words
from lisc.data.meta_data import MetaData

from lisc.collect.time import *

###################################################################################################
###################################################################################################

def test_collect_across_time():

    years = [1950, 1975, 2000]

    # Test with a counts object
    counts = Counts1D()
    counts.add_terms(['language', 'memory'])

    results1 = collect_across_time(counts, years)
    assert results1
    for key, value in results1.items():
        assert key in years
        assert isinstance(value, Counts1D)
        assert counts.has_data

    # Test with a words object
    words = Words()
    words.add_terms(['language', 'memory'])

    results2 = collect_across_time(words, years, retmax=2)
    assert results2
    for key, value in results2.items():
        assert key in years
        assert isinstance(value, Words)
        assert words.has_data
