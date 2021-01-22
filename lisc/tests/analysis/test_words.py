"""Test for the analysis functions for counts, for LISC."""

from collections import Counter

from nltk import FreqDist

from lisc.analysis.words import *

###################################################################################################
###################################################################################################

def test_get_all_values(tarts_all):

    lst = [tarts_all, tarts_all]

    vals = get_all_values(lst, 'dois')
    assert len(vals) == 2*len(tarts_all.dois)

    vals = get_all_values(lst, 'dois', unique=True)
    assert len(vals) == len(set(tarts_all.dois))

def test_get_all_counts(tarts_all):

    lst = [tarts_all, tarts_all]

    # Test Counter, non-combined outputs
    counts = get_all_counts(lst, 'journals')
    assert isinstance(counts, list)
    assert len(counts) == len(lst)

    # Test Counter, combined outputs
    counts = get_all_counts(lst, 'journals', combine=True)
    assert isinstance(counts, Counter)
    assert len(counts) == len(tarts_all.journals)

    # Test FreqDist, non-combined ouputs
    counts = get_all_counts(lst, 'words')
    assert isinstance(counts, list)
    assert len(counts) == len(lst)

    # Test FreqDist, combined ouputs
    counts = get_all_counts(lst, 'words', combine=True)
    assert isinstance(counts, FreqDist)
    assert len(counts) == len(tarts_all.words)
