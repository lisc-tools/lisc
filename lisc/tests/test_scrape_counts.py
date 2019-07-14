"""Tests for scrape counts."""

from lisc.scrape.counts import *

###################################################################################################
###################################################################################################

def test_scrape_counts():

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['protein']]
    terms_b = ['brain']

    counts, percs, a_counts, b_counts, meta_data = scrape_counts(terms_a, excls_a, terms_b)

    assert counts.shape == (2, 1)

    assert len(a_counts) == len(terms_a)
    assert len(b_counts) == len(terms_b)
