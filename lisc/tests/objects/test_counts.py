"""Tests for lisc.objects.counts."""

from lisc.objects.counts import Counts1D, Counts

###################################################################################################
###################################################################################################

## Helper test functions for Counts object

def check_dunders(counts):

    label0 = counts.terms['A'].labels[0]
    label1 = counts.terms['B' if counts.terms['B'].terms else 'A'].labels[0]

    out = counts[label0, label1]
    assert out == counts.counts[(0, 0)]

def check_funcs(counts):

    for dim in ['A'] if counts.square else ['A', 'B', 'both']:
        counts.check_data(dim=dim)
        counts.check_top(dim=dim)
        counts.check_counts(dim=dim)

def drop_data(counts):

    for dim in ['A'] if counts.square else ['A', 'B', 'both']:
        counts.drop_data(10, dim=dim)

def compute_scores(counts):

    counts.compute_score('association')
    assert counts.score.any()
    assert counts.score_info['type'] == 'association'

    for score_type in ['similarity', 'normalize']:
        for dim in ['A'] if counts.square else ['A', 'B']:
            counts.compute_score(score_type, dim=dim)
            assert counts.score.any()
            assert counts.score_info['type'] == score_type
            assert counts.score_info['dim'] == dim

## Counts1D Object

def test_counts1D():

    assert Counts1D()

def test_collect(test_req):

    counts = Counts1D()

    counts.add_terms(['language', 'memory'])
    counts.run_collection(db='pubmed', logging=test_req)

    assert counts.has_data

    assert counts[counts.labels[0]] == counts.counts[0]

    counts.check_top()
    counts.check_counts()

    counts.drop_data(10)

## Counts Object

def test_counts():

    assert Counts()

def test_copy():

    tcounts = Counts()
    ntcounts = tcounts.copy()

    assert ntcounts != tcounts

def test_collect_one(test_req):

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'cell'], term_type='exclusions', dim='A')

    counts.run_collection(db='pubmed', logging=test_req)
    assert counts.has_data

    compute_scores(counts)

    check_dunders(counts)
    check_funcs(counts)
    drop_data(counts)

def test_collect_two(test_req):

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'cell'], term_type='exclusions', dim='A')
    counts.add_terms(['cognition'], dim='B')

    counts.run_collection(db='pubmed', logging=test_req)
    assert counts.has_data

    compute_scores(counts)

    check_dunders(counts)
    check_funcs(counts)
    drop_data(counts)
