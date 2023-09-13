"""Tests for lisc.objects.counts."""

from lisc.objects.counts import Counts1D, Counts

###################################################################################################
###################################################################################################

## Helper test functions

def check_dunders(counts):

    if isinstance(counts, Counts1D):

        label = counts.labels[0]
        out = counts[label0]

        assert out == counts.counts[0]

    if isinstance(counts, Counts):

        label0 = counts.terms['A'].labels[0]
        label1 = counts.terms['B' if counts.terms['B'].terms else 'A'].labels[0]

        out = counts[label0, label1]
        assert out == counts.counts[(0, 0)]

def check_funcs(counts):

    if isinstance(counts, Counts):
        counts.check_data()
    counts.check_top()
    counts.check_counts()

def drop_data(counts):

    counts.drop_data(0)

def compute_scores(counts):

    for score_type in ['normalize', 'association', 'similarity']:
        counts.compute_score(score_type)
        assert counts.score.any()
        assert counts.score_info['type'] == score_type

## Counts1D Object

def test_counts1D():

    assert Counts1D()

def test_collect(test_req):

    counts = Counts1D()

    counts.add_terms(['language', 'memory'])
    counts.run_collection(db='pubmed', logging=test_req)

    assert counts.has_data

    check_funcs(counts)
    drop_data(counts)

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
    counts.add_terms(['protein', 'protein'], term_type='exclusions', dim='A')

    counts.run_collection(db='pubmed', logging=test_req)
    assert counts.has_data

    compute_scores(counts)

    check_dunders(counts)
    check_funcs(counts)
    drop_data(counts)

def test_collect_two(test_req):

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'protein'], term_type='exclusions', dim='A')
    counts.add_terms(['cognition'], dim='B')

    counts.run_collection(db='pubmed', logging=test_req)
    assert counts.has_data

    compute_scores(counts)

    check_dunders(counts)
    check_funcs(counts)
    drop_data(counts)
