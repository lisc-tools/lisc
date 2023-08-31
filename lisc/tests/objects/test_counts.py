"""Tests for lisc.objects.counts."""

from lisc.objects.counts import Counts

###################################################################################################
###################################################################################################

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
    check_funcs(counts)
    drop_data(counts)

def test_collect_two(test_req):

    counts = Counts()

    counts.add_terms(['language', 'memory'], dim='A')
    counts.add_terms(['protein', 'protein'], term_type='exclusions', dim='A')
    counts.add_terms(['cognition'], dim='B')

    counts.run_collection(db='pubmed', logging=test_req)
    assert counts.has_data

    counts.compute_score('normalize')

    compute_scores(counts)
    check_funcs(counts)
    drop_data(counts)

def compute_scores(counts):

    for score_type in ['normalize', 'association', 'similarity']:
        counts.compute_score(score_type)
        assert counts.score.any()
        assert counts.score_info['type'] == score_type

def check_dunders(counts):

    label0 = counts.terms['A'].labels[0]
    label1 = counts.terms['B' if counts.terms['B'].terms else 'A'].labels[0]

    out = counts[label0, label1]
    assert out == self.counts[0, 0]

def check_funcs(counts):

    counts.check_data()
    counts.check_top()
    counts.check_counts()

def drop_data(counts):

    counts.drop_data(0)
