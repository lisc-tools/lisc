"""Tests for scrape counts."""

from lisc.collect.counts import *

###################################################################################################
###################################################################################################

def test_collect_counts():

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['protein']]
    terms_b = ['brain']

    n_a = len(terms_a)
    n_b = len(terms_b)

    cooc, counts, meta_data = collect_counts(terms_a, exclusions_a=excls_a, terms_b=terms_b)

    assert cooc.shape == (n_a, n_b)

    assert len(counts[0]) == n_a
    assert len(counts[1]) == n_b
