"""Tests for lisc.collect.counts."""

from lisc.collect.counts import *

###################################################################################################
###################################################################################################

def test_collect_counts_two(test_req):

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['cell']]
    terms_b = ['brain']

    # Test co-occurence with two terms lists
    cooc, counts, meta_data = collect_counts(\
        terms_a, exclusions_a=excls_a, terms_b=terms_b, logging=test_req)
    assert cooc.shape == (len(terms_a), len(terms_b))
    assert len(counts[0]) == len(terms_a)
    assert len(counts[1]) == len(terms_b)
    assert meta_data.requester['n_requests'] > 0

def test_collect_counts_one(test_req):

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['cell']]

    # Test co-occurence with one list of terms
    cooc, counts, meta_data = collect_counts(\
        terms_a, exclusions_a=excls_a, logging=test_req)
    assert cooc.shape == (len(terms_a), len(terms_a))
    assert len(counts) == len(terms_a)
    assert meta_data.requester['n_requests'] > 0

def test_collect_counts_nocooc(test_req):

    terms_a = ['language', 'memory']
    excls_a = [['protein'], ['cell']]

    # Test coounts without co-occurence
    counts, meta_data = collect_counts(\
        terms_a, exclusions_a=excls_a, collect_coocs=False, logging=test_req)
    assert len(counts) == len(terms_a)
    assert meta_data.requester['n_requests'] > 0
