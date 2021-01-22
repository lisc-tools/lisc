"""Tests for lisc.analysis.words."""

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

    # Test for attribute stored with Counter, with non-combined outputs
    counts = get_all_counts(lst, 'journals')
    assert isinstance(counts, list)
    assert len(counts) == len(lst)

    # Test for attribute stored with Counter, with combined output
    counts = get_all_counts(lst, 'journals', combine=True)
    assert isinstance(counts, Counter)
    assert len(counts) == len(tarts_all.journals)

    # Test for attribute stored with FreqDist, with non-combined ouputs
    counts = get_all_counts(lst, 'words')
    assert isinstance(counts, list)
    assert len(counts) == len(lst)

    # Test for attribute stored with FreqDist, with combined ouput
    counts = get_all_counts(lst, 'words', combine=True)
    assert isinstance(counts, FreqDist)
    assert len(counts) == len(tarts_all.words)
