"""Tests for lisc.analysis.words."""

from collections import Counter

from lisc.analysis.words import *

###################################################################################################
###################################################################################################

def test_get_attribute_counts(twords_full, tarts_full, tarts_none):

    attr = 'dois'

    count = get_attribute_counts(twords_full, attr)
    assert count == sum([len(getattr(res, attr)) for res in twords_full.results])

    count = get_attribute_counts([tarts_full, tarts_full], attr)
    assert count == len(getattr(tarts_full, attr)) * 2

    count = get_attribute_counts([tarts_none, tarts_none], attr)
    assert count == len(getattr(tarts_none, attr)) * 2 - 2


def test_get_all_values(twords_full, tarts_full, tarts_none):

    attr = 'dois'

    values = get_all_values(twords_full, attr)

    lst = [tarts_full, tarts_full]
    vals = get_all_values(lst, 'dois')
    assert len(vals) == 2 * len(tarts_full.dois)

    vals = get_all_values(lst, 'dois', unique=True)
    assert len(vals) == len(set(tarts_full.dois))

def test_get_all_counts(twords_full, tarts_all):

    attr = 'words'

    ## Test ArticlesAll input
    lst = [tarts_all, tarts_all]

    # Test for non-combined outputs
    counts = get_all_counts(lst, attr)
    assert isinstance(counts, list)
    assert len(counts) == len(lst)

    # Test for combined output
    counts = get_all_counts(lst, attr, combine=True)
    assert isinstance(counts, Counter)
    assert len(counts) == len(tarts_all.words)

    ## Test words input
    counts = get_all_counts(twords_full, attr)
    assert isinstance(counts, list)
