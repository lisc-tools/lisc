"""Tests for lisc.collect.counts."""

from lisc.collect.counts import *

###################################################################################################
###################################################################################################

def test_collect_counts():

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['protein']]
    terms_b = ['brain']

    # Test co-occurence with two terms lists
    cooc, counts, meta_data = collect_counts(terms_a, exclusions_a=excls_a, terms_b=terms_b)
    assert cooc.shape == (len(terms_a), len(terms_b))
    assert len(counts[0]) == len(terms_a)
    assert len(counts[1]) == len(terms_b)
    assert meta_data.requester['n_requests'] > 0

    # Test co-occurence with one list of terms
    cooc, counts, meta_data = collect_counts(terms_a, exclusions_a=excls_a)
    assert cooc.shape == (len(terms_a), len(terms_a))
    assert len(counts) == len(terms_a)
    assert meta_data.requester['n_requests'] > 0

    # Test coounts without co-occurence
    counts, meta_data = collect_counts(terms_a, exclusions_a=excls_a, terms_b=terms_b)
    assert len(counts) == len(terms_a)
    assert meta_data.requester['n_requests'] > 0
