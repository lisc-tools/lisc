"""Tests for scrape counts."""

from lisc.scrape.counts import *

###################################################################################################
###################################################################################################

def test_scrape_counts():

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['protein']]
    terms_b = ['brain']

    n_a = len(terms_a)
    n_b = len(terms_b)

    cooc, counts, meta_data = scrape_counts(terms_a, excls_a, terms_b)

    assert cooc.shape == (n_a, n_b)

    assert len(counts[0]) == n_a
    assert len(counts[1]) == n_b
